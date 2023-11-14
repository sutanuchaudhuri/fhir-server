const patient = require('./fixtures/patient/patient1.json');
const { describe, expect, test } = require('@jest/globals');
const {DeidentificationManager} = require('../../deidentification/deidentificationManager');

describe('deindentificationManager Tests', () => {
    describe('deindentificationManager Tests', () => {
        test('getPatientIdFromResourceAsync works for Patient', async () => {
            const deindentificationManager = new DeidentificationManager();
            const deidentifiedResource = deindentificationManager.deidentify(
                {
                    resource: patient
                }
            );
            expect(deidentifiedResource).toStrictEqual('subject');
        });
    });
});
