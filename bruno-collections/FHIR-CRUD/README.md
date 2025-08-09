# FHIR CRUD Operations - Bruno API Collection

This Bruno collection provides comprehensive testing for FHIR R4 CRUD operations including authentication, Patient management, Observations, Practitioners, and Organizations.

## 🚀 Quick Start

### Prerequisites

1. **FHIR Server Running**: Ensure your FHIR server is running on `http://localhost:3000`
2. **Authentication**: You need a valid JWT token from Auth0 or another configured identity provider
3. **Bruno API Client**: Install [Bruno](https://usebruno.com/) to run this collection

### Authentication Setup

The FHIR server validates tokens using JWKS (JSON Web Key Set) from configured identity providers. To test the APIs, you need:

#### Option 1: Real Auth0 Token (Recommended)
1. Get a valid token from Auth0 using client credentials flow:
```bash
curl -X POST "https://dev-xjawa6dpvqw14cl6.us.auth0.com/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "your_real_client_id",
    "client_secret": "your_real_client_secret",
    "audience": "https://fhir-server",
    "grant_type": "client_credentials"
  }'
```

2. Use the returned `access_token` in the collection

#### Option 2: Update Environment Variables
1. Open `environments/Local.bru`
2. Replace `clientId` and `clientSecret` with your real Auth0 credentials
3. Run the "Get Auth Token" request to automatically authenticate

## 📁 Collection Structure

```
FHIR-CRUD/
├── environments/
│   └── Local.bru           # Environment variables and configuration
├── Get Auth Token.bru      # Authentication endpoint
├── Get Server Metadata.bru # FHIR server capabilities
├── Run All CRUD Tests.bru  # Test runner and instructions
├── Patient/                # Patient CRUD operations
│   ├── Create Patient.bru
│   ├── Read Patient.bru
│   ├── Update Patient.bru
│   ├── Search Patients.bru
│   └── Delete Patient.bru
├── Observation/           # Observation CRUD operations
│   ├── Create Observation.bru
│   ├── Read Observation.bru
│   ├── Update Observation.bru
│   ├── Search Observations.bru
│   └── Delete Observation.bru
├── Practitioner/          # Practitioner operations
│   ├── Create Practitioner.bru
│   └── Read Practitioner.bru
└── Organization/          # Organization operations
    └── Create Organization.bru
```

## 🔄 How to Run

### Method 1: Individual Requests
1. Open Bruno and load this collection
2. First run "Get Auth Token" to authenticate
3. Run individual CRUD operations as needed

### Method 2: Full Test Suite
1. Run "Get Auth Token" first
2. Execute requests in this order:
   - Patient: Create → Read → Update → Search → Delete
   - Observation: Create → Read → Update → Search → Delete
   - Practitioner: Create → Read
   - Organization: Create

### Method 3: Run Collection (if supported)
Use Bruno's "Run Collection" feature to execute all requests automatically.

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `baseUrl` | FHIR server base URL | `http://localhost:3000` |
| `fhirVersion` | FHIR version | `4_0_0` |
| `authToken` | JWT bearer token | Set automatically by auth script |
| `clientId` | Auth0 client ID | Your Auth0 application ID |
| `clientSecret` | Auth0 client secret | Your Auth0 application secret |
| `authUrl` | Token endpoint | `https://dev-xjawa6dpvqw14cl6.us.auth0.com/oauth/token` |
| `audience` | Token audience | `https://fhir-server` |

## 📊 What Each Operation Tests

### Patient CRUD
- **Create**: Creates a patient with name, gender, birthDate, and contact info
- **Read**: Retrieves the created patient by ID
- **Update**: Modifies patient information (adds phone number)
- **Search**: Searches patients by family name
- **Delete**: Removes the patient from the system

### Observation CRUD
- **Create**: Creates a vital signs observation (heart rate) linked to patient
- **Read**: Retrieves the observation by ID
- **Update**: Modifies the observation value
- **Search**: Searches observations by patient and category
- **Delete**: Removes the observation

### Practitioner
- **Create**: Creates a practitioner with qualifications and contact info
- **Read**: Retrieves practitioner details

### Organization
- **Create**: Creates a healthcare organization with contact information

## 🐛 Troubleshooting

### Authentication Issues
- **"Unauthorized"**: Check your token validity and audience
- **"Invalid token"**: Ensure you're using a token signed by a configured identity provider
- **"Expired token"**: Get a new token using the "Get Auth Token" request

### Request Issues
- **"Resource not found"**: Ensure you create resources before trying to read/update them
- **Variables not set**: Check that authentication was successful and variables are populated

### Server Issues
- **Connection refused**: Ensure FHIR server is running on the configured port
- **Timeout**: Check server health and network connectivity

## 📝 Test Token Information

The collection includes a test token for demonstration purposes, but it won't work with JWKS validation. The test token includes:

- **Issuer**: Auth0 domain
- **Audience**: `https://fhir-server`
- **Scopes**: `patient/*.* user/*.* system/*.*`
- **Patient Access**: Patient ID "123"
- **Expiry**: 24 hours from generation

For real testing, replace with a valid token from your identity provider.

## 🔍 Viewing Results

Each request includes post-response scripts that:
- Log important information to the console
- Store resource IDs for subsequent requests
- Provide clear success/failure feedback
- Extract and display key resource data

Check the Bruno console for detailed execution logs.

## 🌐 FHIR Resources Covered

This collection demonstrates operations on core FHIR R4 resources:

- **Patient**: Demographics and contact information
- **Observation**: Clinical measurements and vital signs
- **Practitioner**: Healthcare providers and their qualifications
- **Organization**: Healthcare organizations and facilities

Each resource follows FHIR R4 specification and includes realistic test data.
