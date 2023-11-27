const patient = require('./fixtures/patient/patient1.json');
const {describe, expect, test} = require('@jest/globals');
const {DeidentificationManager} = require('../../deidentification/deidentificationManager');
const Patient = require('../../fhir/classes/4_0_0/resources/patient');
const fhirpath = require('fhirpath');
// For FHIR model data (choice type support) pull in the model file:
const fhirpath_r4_model = require('fhirpath/fhir-context/r4');

describe('deindentificationManager Tests', () => {
    describe('deindentificationManager Tests', () => {
        test('test 1', async () => {
            // Your FHIR JSON object
            const fhirJsonObject = {
                resourceType: 'Patient',
                name: [
                    {
                        given: ['subject']
                    }
                ]
            };

            // Your FHIRPath expression
            const fhirPathExpression = 'Patient.name.given';
            // const fhirPathExpression = 'name.given';

            const result1 = new DeidentificationManager().findField(fhirPathExpression, fhirJsonObject);
            console.log(result1);

        });
        test('test for given name with full resource', async () => {

            // Your FHIRPath expression
            const fhirPathExpression = 'Patient.name.given';
            // const fhirPathExpression = 'name.given';

            const result1 = new DeidentificationManager().findFieldInResource(fhirPathExpression, new Patient(patient));
            console.log(result1);
            expect(result1).toStrictEqual([['SHYLA']]);
        });
        test('test for family with full resource', async () => {

            // Your FHIRPath expression
            const fhirPathExpression = 'Patient.name.family';
            // const fhirPathExpression = 'name.given';

            const result1 = new DeidentificationManager().findFieldInResource(fhirPathExpression, new Patient(patient));
            console.log(result1);
            expect(result1).toStrictEqual(['PATIENT1']);
        });
        test('test findNodeByType', async () => {
            const result1 = new DeidentificationManager().findNodeByType(new Patient(patient), 'HumanName');
            console.log(result1);
            expect(result1).toStrictEqual(['PATIENT1']);
        });
        test('test for nodesByType with full resource', async () => {

            // Your FHIRPath expression
            const fhirPathExpression = "nodesByType('HumanName').given";
            // const fhirPathExpression = 'name.given';

            const result1 = new DeidentificationManager().findFieldInResource(fhirPathExpression, new Patient(patient));
            console.log(result1);
            expect(result1).toStrictEqual(['PATIENT1']);
        });
        test('test 2', async () => {
            // Your FHIR JSON object
            const fhirJsonObject = {
                resourceType: 'Patient',
                name: [
                    {
                        given: ['subject']
                    }
                ]
            };

            // Your FHIRPath expression
            const fhirPathExpression = 'Patient.name.given';

            let tracefunction = function (x, label) {
                console.log('Trace output [' + label + ']: ', x);
            };

            // Evaluate the FHIRPath expression against the FHIR resource
            /**
             * table
             * @type import("fhirpath").UserInvocationTable
             */
            let userInvocationTable = {
                pow: {
                    fn: function (inputs) {
                        return inputs.map(i => i);
                    },
                    arity: {0: [], 1: ['Integer']},
                    internalStructures: true
                }
            };
            let options = {
                traceFn: tracefunction,
                userInvocationTable: userInvocationTable
            };
            const result = fhirpath.evaluate(fhirJsonObject, fhirPathExpression,
                null, fhirpath_r4_model, options);

            // Output the result
            console.log(result);
        });
        test('test 3', async () => {
            // Your FHIR JSON object
            const deindentificationManager = new DeidentificationManager();
            const deidentifiedResource = deindentificationManager.deidentify(
                {
                    resource: new Patient(patient)
                }
            );
            expect(deidentifiedResource).toStrictEqual('subject');
        });
    });
});
