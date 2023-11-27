const config = require('./config.json');
// https://github.com/hl7/fhirpath.js/
// const fhirpath = require('fhirpath');
// For FHIR model data (choice type support) pull in the model file:
// const fhirpath_r4_model = require('fhirpath/fhir-context/r4');


class DeidentificationManager {
    constructor() {
        this.config = config;
    }

    /**
     * Deidentification
     * @param {Resource} resource
     * @returns {Resource}
     */
    deidentify({resource}) {
        this.visit(resource, ['']);
        return resource;
    }

    /**
     * visitor pattern
     * @param {Object|Object[]} node
     * @param {string[]} path
     */
    visit(node, path) {
        if (Array.isArray(node)) {
            node.forEach((item, _) => this.visit(item, path.slice(1)));
        } else if (typeof node === 'object' && node !== null) {
            Object.keys(node).forEach(key => {
                const newPath = path.slice(1);
                /**
                 * type: string
                 */
                const matchingRules = this.findMatchingRules({path: newPath, node: node[`${key}`]});
                if (matchingRules.length > 0) {
                    node[`${key}`] = null; // Redact the node by setting it to null
                } else {
                    this.visit(node[`${key}`], newPath); // Continue traversal
                }
            });
        }
    }

    /**
     * Find matching rules
     * @param {string[]} path
     * @param {Object} node
     * @returns {Object}
     */
    // eslint-disable-next-line no-unused-vars
    findMatchingRules({path, node}) {
        return this.config.fhirPathRules.filter(rule => {
            return path.endsWith(rule.type);
        });
    }

    /**
     * Find a field in a resource
     * @param {string} path
     * @param {Object} resource
     * @returns {*}
     */
    findField(path, resource) {
        // Split the path into parts
        /**
         * @type {string[]}
         */
        const parts = path.split('.');

        /**
         * @type {string}
         */
        const resourceName = parts.shift();

        if (resource.resourceType !== resourceName) {
            return undefined;
        }

        // Recursive function to traverse the resource
        // noinspection TailRecursionJS
        function traverse(currentResource, pathParts) {
            // Base case: if no more path parts, return the current resource
            if (pathParts.length === 0) {
                return currentResource;
            }

            // Take the next part of the path
            /**
             * @type {string}
             */
            const nextPart = pathParts.shift();

            // If the current resource is an array, iterate over it and apply the traversal to each element
            if (Array.isArray(currentResource)) {
                return currentResource.map(element => traverse(element, [...pathParts]));
            }

            // If the current resource is an object, continue the traversal
            if (currentResource && typeof currentResource === 'object') {
                if (nextPart in currentResource) {
                    if (pathParts.length > 0) {
                        return traverse(currentResource[`${nextPart}`], pathParts);
                    } else {
                        // we're at the end of the path so look for a field
                        return currentResource.get(`${nextPart}`);
                    }
                } else {
                    return undefined;
                }
            }

            // If the path is incorrect or field does not exist, return undefined
            return undefined;
        }

        // Start the traversal with the full resource and the path parts
        return traverse(resource, parts);
    }

    /**
     * Find a field in a resource
     * @param {string} path
     * @param {Resource} resource
     * @returns {*}
     */
    findFieldInResource(path, resource) {
        const regexToParseNodesByType = /nodesByType\('([^']+)'\)/;
        // Split the path into parts
        /**
         * @type {string[]}
         */
        const parts = path.split('.');

        /**
         * @type {RegExpMatchArray}
         */
        const nadesByTypeMatch = path.match(regexToParseNodesByType);

        /**
         * @type {string|undefined}
         */
        let elementType;
        if (nadesByTypeMatch) {
            /**
             * @type {string}
             */
            elementType = nadesByTypeMatch[1];
            parts.shift();
        } else {

            /**
             * @type {string}
             */
            const resourceName = parts.shift();

            if (resource.resourceType !== resourceName) {
                return undefined;
            }
        }

        // Recursive function to traverse the resource
        // noinspection TailRecursionJS
        /**
         * traverse
         * @param {Object|Object[]} currentField
         * @param {string[]} pathParts
         * @param {string|undefined} elementType1
         * @returns {undefined|*}
         */
        function traverse({currentField, pathParts, elementType1}) {
            // Base case: if no more path parts, return the current resource
            if (pathParts.length === 0) {
                return currentField;
            }

            // Take the next part of the path
            /**
             * @type {string}
             */
            const nextPart = pathParts.shift();

            // If the current resource is an array, iterate over it and apply the traversal to each element
            if (Array.isArray(currentField)) {
                if (pathParts.length > 0) {
                    return currentField.map(element => traverse(
                            {
                                currentField: element,
                                pathParts: [...pathParts],
                                elementType1: elementType1
                            }
                        )
                    );
                } else {
                    // we're at the end of the path so look for a field
                    return currentField.map(element => element[`${nextPart}`]);
                }
            }

            // If the current resource is an object, continue the traversal
            if (currentField && typeof currentField === 'object') {
                if (nextPart in currentField) {
                    if (pathParts.length > 0) {
                        return traverse(
                            {
                                currentField: currentField[`${nextPart}`],
                                pathParts: pathParts,
                                elementType1: elementType1
                            }
                        );
                    } else {
                        // we're at the end of the path so look for a field
                        return currentField[`${nextPart}`];
                    }
                } else {
                    return undefined;
                }
            }

            // If the path is incorrect or field does not exist, return undefined
            return undefined;
        }

        // Start the traversal with the full resource and the path parts
        return traverse({currentField: resource, pathParts: parts, elementType1: elementType});
    }

    /**
     *
     * @param {Object} node
     * @param {string} nodeType
     * @returns {Object[]}
     */
    findNodeByType(node, nodeType) {
        if (Array.isArray(node)) {
            return node.flatMap(item => this.findNodeByType(item, nodeType))
                .filter(item => item !== undefined && !(Array.isArray(item) && item.length === 0));
        } else if (typeof node === 'object' && node !== null) {
            if (node.constructor.name === nodeType) {
                return [node];
            }
            return Object.keys(node).flatMap(key => this.findNodeByType(node[`${key}`], nodeType))
                .filter(item => item !== undefined && !(Array.isArray(item) && item.length === 0));
        } else {
            return undefined;
        }
    }
}

module.exports = {
    DeidentificationManager
};
