# CounterApp-BackEnd-Lambda
This package implements the API handler Lambda function for [CounterApp BackEnd](https://github.com/rubikvn2100/CounterApp-BackEnd). It facilitates user interactions for viewing or modifying the counter value. Each session, triggered by a user's request, remains active for a predetermined period. Importantly, all counter requests necessitate a session token for authentication. Updating the counter value also prolongs the session's active duration.

## API Endpoints
The Lambda function handles the following API endpoints:

### 1. Create User Session

* **Endpoint:** `POST /api/session`

* **Description:** Creates a new user session.

* **Response:**

    * `200`: A new session is created. The response includes a 32-character token and the session duration in seconds.

    ```
    {
        "statusCode": 200,
        "body": {
            "token": "01234567890123456789012345678901",
            "sessionDuration": 300
        }
    }
    ```

    * `409`: Cannot create new session.

### 2. Get Counter Value

* **Endpoint:** `GET /api/counter`

* **Description:** Retrieves the current counter value.

* **Authorization:**

  - Required

  - Type: Bearer Token

  - Header: `Authorization: Bearer <token>`

* **Response:**

    * `200`: Successfully retrieved the counter value.

    ```
    {
        "statusCode": 200,
        "body": {
            "counter": 999
        }
    }
    ```

    * `401`: Unauthorized.

    * `403`: Token expired.

    * `404`: Token not found.

### 3. Updates the counter value.

* **Endpoint:** `POST /api/counter`

* **Description:** Updates the counter value. A valid request refreshes the token with a new expiration set to the request time plus the session duration

* **Authorization:**

  - Required

  - Type: Bearer Token

  - Header: `Authorization: Bearer <token>`

* **Body:**

    ```
    {
        "timestamps": <A list of timestamps.>
    }
    ```

* **Response:**

    * `200`: Successfully update and the new counter value is send back.

    ```
    {
        "statusCode": 200,
        "body": {
            "counter": 999
        }
    }
    ```

    * `400`: Bad request.

    * `401`: Unauthorized.

    * `403`: Token expired.

    * `404`: Token not found.

    * `422`: invalid timestamp sequence.

## Environment Variables
The Lambda function requires the following environment variables to be set:

* **TABLE_NAME**
* **SESSION_DURATION**
* **ALLOW_ORIGINS**
* **ACCESS_CONTROL_MAX_AGE**

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