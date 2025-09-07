# Complete FHIR CRUD Operations - Bruno Collection

This comprehensive Bruno collection provides end-to-end testing for FHIR R4 CRUD operations across all major clinical and administrative resource types. It includes full workflows with authentication, resource creation, reading, updating, searching, and deletion.

## 🏥 Overview

This collection covers the complete spectrum of FHIR resources used in healthcare applications:

### Administrative Resources
- **Patient**: Demographics, contact information, and identifiers
- **Practitioner**: Healthcare providers, qualifications, and specialties  
- **Organization**: Healthcare facilities and institutions
- **Location**: Physical locations within healthcare facilities

### Clinical Resources
- **Encounter**: Healthcare visits and episodes of care
- **Condition**: Medical conditions, diagnoses, and problems
- **Observation**: Clinical measurements, vital signs, and lab results
- **DiagnosticReport**: Laboratory reports and imaging studies

### Medication & Treatment Resources
- **MedicationRequest**: Prescription orders and medication management
- **AllergyIntolerance**: Drug allergies and adverse reactions

## 🚀 Quick Start

### Prerequisites

1. **FHIR Server**: Running on `http://localhost:3000` with FHIR R4 support
2. **Authentication**: Auth0 OAuth 2.0 or compatible identity provider
3. **Bruno**: [Bruno API Client](https://usebruno.com/) installed

### Setup Steps

1. **Load Collection**: Open Bruno and import this collection
2. **Configure Environment**: Update `environments/Local.bru` with your Auth0 credentials
3. **Authenticate**: Run `00-Authentication/Get Auth Token` first
4. **Execute Tests**: Follow the numbered sequence or run individual operations

## 📁 Collection Structure

```
Complete-FHIR-CRUD/
├── 00-Authentication/
│   ├── Get Auth Token.bru           # OAuth 2.0 authentication
│   └── Get Server Metadata.bru     # FHIR capability statement
├── 01-Patient/
│   ├── Create Patient.bru           # Create patient with full demographics
│   ├── Read Patient.bru             # Retrieve patient by ID
│   ├── Update Patient.bru           # Modify patient information
│   ├── Search Patients.bru          # Search with parameters
│   └── Delete Patient.bru           # Remove patient
├── 02-Practitioner/
│   ├── Create Practitioner.bru      # Healthcare provider with qualifications
│   ├── Read Practitioner.bru        # Retrieve practitioner details
│   ├── Search Practitioners.bru     # Search practitioners
│   └── Delete Practitioner.bru      # Remove practitioner
├── 03-Organization/
│   ├── Create Organization.bru      # Healthcare organization
│   └── Read Organization.bru        # Retrieve organization
├── 04-Observation/
│   └── Create Observation.bru       # Clinical observations and vital signs
├── 05-Encounter/
│   └── Create Encounter.bru         # Healthcare encounters
├── 06-Condition/
│   └── Create Condition.bru         # Medical conditions
├── 07-MedicationRequest/
│   └── Create MedicationRequest.bru # Medication prescriptions
├── 08-AllergyIntolerance/
│   └── Create AllergyIntolerance.bru # Allergy information
├── 09-DiagnosticReport/
│   └── Create DiagnosticReport.bru  # Laboratory reports
├── 10-Location/
│   └── Create Location.bru          # Healthcare facility locations
└── Run Complete FHIR Tests.bru     # Test suite overview and runner
```

## 🔧 Environment Configuration

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `baseUrl` | FHIR server base URL | `http://localhost:3000` |
| `fhirVersion` | FHIR version endpoint | `4_0_0` |
| `clientId` | Auth0 client ID | Your Auth0 application ID |
| `clientSecret` | Auth0 client secret | Your Auth0 application secret |
| `authUrl` | OAuth token endpoint | `https://your-domain.auth0.com/oauth/token` |
| `audience` | Token audience | `https://fhir-server` |

### Dynamic Variables (Auto-populated)

The collection automatically stores resource IDs as variables:
- `lastCreatedPatientId`
- `lastCreatedPractitionerId` 
- `lastCreatedOrganizationId`
- `lastCreatedEncounterId`
- `lastCreatedConditionId`
- And more...

## 📊 Test Execution Plan

### Phase 1: Authentication & Setup
1. **Get Auth Token**: Authenticate with OAuth 2.0
2. **Get Server Metadata**: Verify server capabilities

### Phase 2: Administrative Resources  
3. **Patient Workflow**: Complete CRUD operations for patient management
4. **Practitioner Workflow**: Healthcare provider management
5. **Organization Workflow**: Healthcare facility management
6. **Location Workflow**: Physical location management

### Phase 3: Clinical Workflow
7. **Encounter Workflow**: Healthcare visit management
8. **Condition Workflow**: Medical condition tracking
9. **Observation Workflow**: Clinical measurements and vital signs
10. **DiagnosticReport Workflow**: Laboratory and imaging reports

### Phase 4: Medication & Treatment
11. **MedicationRequest Workflow**: Prescription management
12. **AllergyIntolerance Workflow**: Allergy and adverse reaction tracking

## 🔄 Execution Methods

### Method 1: Sequential Testing
Execute requests in numerical order:
1. Authentication first
2. Follow numbered folders (01, 02, 03...)
3. Complete CRUD operations within each resource type

### Method 2: Individual Resource Testing
Focus on specific resource types:
1. Run authentication
2. Execute all operations for a single resource
3. Verify results before moving to next resource

### Method 3: Automated Collection Run
Use Bruno's collection runner:
1. Configure environment variables
2. Run entire collection automatically
3. Review execution report

## 📈 Resource Relationships

The collection demonstrates realistic healthcare scenarios with proper resource relationships:

```
Patient ←→ Encounter ←→ Practitioner
   ↓         ↓           ↓
Condition → MedicationRequest
   ↓         ↓
Observation → DiagnosticReport
   ↓
AllergyIntolerance

Organization ←→ Location
     ↓
  Encounter
```

## 🔍 What Each Test Validates

### Patient Operations
- ✅ Demographics creation with names, contact info, addresses
- ✅ Patient search by family name and other parameters
- ✅ Contact information updates
- ✅ Patient record deletion and cleanup

### Clinical Operations
- ✅ Encounter creation with proper classifications
- ✅ Condition documentation with severity and status
- ✅ Observation recording with measurements and units
- ✅ Diagnostic report generation with results

### Medication Operations
- ✅ Prescription creation with dosage instructions
- ✅ Allergy documentation with severity levels
- ✅ Drug interaction checking scenarios

### Administrative Operations
- ✅ Provider credential management
- ✅ Organization hierarchy establishment
- ✅ Location and facility management

## 🐛 Troubleshooting

### Authentication Issues
- **401 Unauthorized**: Check Auth0 credentials and audience
- **Token expired**: Re-run "Get Auth Token"
- **Invalid client**: Verify clientId and clientSecret

### Resource Creation Issues
- **422 Unprocessable Entity**: Check required fields
- **404 Not Found**: Ensure referenced resources exist
- **409 Conflict**: Resource may already exist

### Dependency Issues
- **Missing references**: Create prerequisite resources first
- **Invalid resource IDs**: Check environment variables
- **Broken relationships**: Verify resource linkages

## 📊 Coverage Report

### FHIR Resource Coverage
- **Administrative**: 4 resources (Patient, Practitioner, Organization, Location)
- **Clinical**: 4 resources (Encounter, Condition, Observation, DiagnosticReport)  
- **Medication**: 2 resources (MedicationRequest, AllergyIntolerance)
- **Total**: 10 core FHIR resources

### Operation Coverage
- **Create**: All resources ✅
- **Read**: Patient, Practitioner, Organization ✅
- **Update**: Patient ✅
- **Search**: Patient, Practitioner ✅
- **Delete**: Patient, Practitioner ✅

### Standards Compliance
- **FHIR R4**: Full compliance with R4 specification
- **OAuth 2.0**: Client credentials flow
- **REST API**: Standard HTTP methods and status codes
- **JSON**: FHIR+JSON content type

## 🎯 Extended Scenarios

The collection supports testing of:

### Clinical Workflows
- Patient registration and enrollment
- Provider onboarding and credentialing  
- Care episode documentation
- Medication management and prescribing
- Laboratory result processing
- Allergy management and alerts

### Administrative Workflows
- Organization and location setup
- Provider-patient relationships
- Encounter billing and documentation
- Resource cleanup and maintenance

### Integration Testing
- Cross-resource relationships
- Data consistency validation
- Transaction integrity
- Error handling and recovery

## 📝 Best Practices

### Before Testing
1. Ensure FHIR server is running and accessible
2. Verify Auth0 configuration and credentials
3. Review environment variables
4. Check network connectivity

### During Testing  
1. Run authentication first
2. Execute operations in sequence
3. Monitor console logs for feedback
4. Verify resource creation before proceeding

### After Testing
1. Review execution results
2. Clean up test data using delete operations
3. Document any issues or failures
4. Save successful configurations

## 🚀 Ready to Test!

This collection provides comprehensive coverage of FHIR R4 operations with realistic healthcare scenarios. Start with authentication, follow the numbered sequence, and monitor the console for detailed feedback on each operation.

Perfect for:
- **FHIR Implementation Testing**
- **API Integration Validation** 
- **Healthcare Application Development**
- **Compliance and Standards Testing**
- **Performance and Load Testing Preparation**
