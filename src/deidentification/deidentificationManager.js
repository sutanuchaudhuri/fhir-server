const config = require('./config.json');

class DeidentificationManager {
    constructor() {
        this.config = config;
    }

    /**
     * Deidentification
     * @param resource
     * @returns {resource}
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
                if (this.shouldRedact(newPath)) {
                    if (key === 'extension' || key === 'name' && newPath.endsWith('HumanName')) {
                        node[`${key}`] = null; // Redact the node by setting it to null
                    }
                } else {
                    this.visit(node[`${key}`], newPath); // Continue traversal
                }
            });
        }
    }

    shouldRedact(path) {
        return this.config.fhirPathRules.some(rule => {
            if (rule.method === 'redact') {
                return path.endsWith(rule.type);
            }
            return false;
        });
    }
}

module.exports = {
    DeidentificationManager
};
