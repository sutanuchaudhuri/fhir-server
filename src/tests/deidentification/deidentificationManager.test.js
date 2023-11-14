const patient = require('./fixtures/patient/patient1.json');
const { describe, expect, test } = require('@jest/globals');
const {DeidentificationManager} = require('../../deidentification/deidentificationManager');
const Patient = require('../../fhir/classes/4_0_0/resources/patient');

describe('deindentificationManager Tests', () => {
    describe('deindentificationManager Tests', () => {
        test('getPatientIdFromResourceAsync works for Patient', async () => {
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
