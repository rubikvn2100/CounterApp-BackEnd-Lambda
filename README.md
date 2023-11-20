# CounterApp-BackEnd-Lambda
This package implements the API handler Lambda function for [CounterApp BackEnd](https://github.com/rubikvn2100/CounterApp-BackEnd). It facilitates user interactions for viewing or modifying the counter value. Each session, triggered by a user's request, remains active for a predetermined period. Importantly, all counter requests necessitate a session token for authentication. Updating the counter value also prolongs the session's active duration.

## API Endpoints
The Lambda function handles the following API endpoints:

* **GET /api/counter**: Fetches the current counter value.
* **POST /api/counter**: Updates the counter value.
* **POST /api/session**: Creates a new user session.

## Environment Variables
The Lambda function requires the following environment variables to be set:

* **TABLE_NAME**
* **SESSION_DURATION**

## Development and Testing
The package includes **setup_and_testh.sh** for automated testing.

To deploy the test, run:

```
./setup_and_test.sh
```

This script offers the following options:

* **--coverage**: Run coverage tests
* **--html**: Generate an HTML coverage report (requires --coverage)
* **--help**: Display this help message