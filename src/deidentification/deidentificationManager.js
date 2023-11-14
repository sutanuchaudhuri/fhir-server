const config = require('./config.json');

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
        this.visit(resource, '');
        return resource;
    }

    /**
     * visitor pattern
     * @param {Object|Object[]} node
     * @param {string} path
     */
    visit(node, path) {
        if (Array.isArray(node)) {
            node.forEach((item, index) => this.visit(item, `${path}[${index}]`));
        } else if (typeof node === 'object' && node !== null) {
            Object.keys(node).forEach(key => {
                const newPath = `${path}.${key}`.replace(/^\./, ''); // Remove leading dot
                /**
                 * type: string
                 */
                const matchingRules = this.findMatchingRules({path: newPath});
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
     * @param {string} path
     * @returns {Object}
     */
    findMatchingRules({path}) {
        return this.config.fhirPathRules.filter(rule => {
            return path.endsWith(rule.type);
        });
    }
}

module.exports = {
    DeidentificationManager
};
