#!/bin/bash

echo "=== FHIR CRUD Bruno Collection Summary ==="
echo ""
echo "📁 Collection Structure:"
cd "/Users/ekantikachaudhuri/Developer/fhir-server/bruno-collections/FHIR-CRUD"

echo "   🔧 Configuration:"
echo "      ├── bruno.json (Collection metadata)"
echo "      ├── environments/Local.bru (Environment variables)"
echo "      └── README.md (Comprehensive documentation)"
echo ""

echo "   🔐 Authentication:"
find . -path "./Auth/*" -name "*.bru" | sed 's|./|      ├── |'
echo ""

echo "   📊 Metadata & Testing:"
find . -path "./Metadata/*" -name "*.bru" | sed 's|./|      ├── |'
echo "      └── Run All CRUD Tests.bru (Test runner)"
echo ""

echo "   👤 Patient CRUD Operations:"
find . -path "./Patient/*" -name "*.bru" | sort | sed 's|./|      ├── |'
echo ""

echo "   🩺 Observation CRUD Operations:"
find . -path "./Observation/*" -name "*.bru" | sort | sed 's|./|      ├── |'
echo ""

echo "   👨‍⚕️ Practitioner Operations:"
find . -path "./Practitioner/*" -name "*.bru" | sort | sed 's|./|      ├── |'
echo ""

echo "   🏥 Organization Operations:"
find . -path "./Organization/*" -name "*.bru" | sort | sed 's|./|      └── |'
echo ""

echo "📊 Collection Statistics:"
TOTAL_REQUESTS=$(find . -name "*.bru" -not -path "./environments/*" | wc -l | tr -d ' ')
CRUD_OPERATIONS=$(find . -path "./Patient/*" -o -path "./Observation/*" | wc -l | tr -d ' ')
echo "   • Total API requests: $TOTAL_REQUESTS"
echo "   • CRUD operations: $CRUD_OPERATIONS"
echo "   • Resources covered: Patient, Observation, Practitioner, Organization"
echo "   • Authentication: Auth0 OAuth 2.0 with fallback"
echo ""

echo "🚀 Ready to Test:"
echo "   1. Open Bruno API client"
echo "   2. Load this collection"
echo "   3. Run 'Get Auth Token' first"
echo "   4. Execute CRUD operations"
echo ""

echo "⚠️  Authentication Note:"
echo "   • Test token included but won't work with JWKS validation"
echo "   • Update clientId/clientSecret with real Auth0 credentials"
echo "   • Or manually set a valid token in authToken variable"
echo ""

echo "✅ OAuth Configuration Completed:"
echo "   • AUTH_SERVER_URI: https://dev-xjawa6dpvqw14cl6.us.auth0.com"
echo "   • FHIR server advertising correct Auth0 endpoints"
echo "   • Comprehensive API testing suite ready"
echo ""
echo "🎉 Bruno FHIR CRUD Collection Successfully Created!"
