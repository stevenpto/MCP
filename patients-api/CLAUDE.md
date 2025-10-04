# Patient Data MCP Tool — Product Requirements Document (PRD)

## Objective
Enable the AI Optometry/Ophthalmology Agent to securely retrieve and summarize patient, prescription, appointment, and imaging data through REST API `GET` endpoints from the Eye2Eye backend server.

## Overview
This MCP tool provides **read-only access** to the Eye2Eye backend API. It allows the agent to query specific patient data, inventory, and reports.  
The tool will handle authentication, make HTTP GET requests, and return structured JSON results to the LLM for reasoning and summarization.

---

## API Host
`http://<internal-ip>:5005`

---

## Endpoints to Expose

### 1. **Patient Endpoints**
| Name | Endpoint | Method | Params | Description |
|------|-----------|---------|---------|-------------|
| `get_all_patients` | `/patients` | GET | — | Retrieve all patient profiles |
| `get_patient_by_id` | `/patients/{id}` | GET | `id` (int) | Retrieve patient record by ID |
| `get_patient_by_name` | `/patient` | GET | `first_name`, `last_name` | Search by patient name |
| `get_patients_by_birthday_month` | `/reports/birthday/{month}` | GET | `month` (1–12) | Patients with birthdays in a given month |
| `get_patients_by_insurance_type` | `/reports/insurance?insurance_type={type}` | GET | `insurance_type` | Filter patients by insurance provider |
| `get_insurance_types` | `/reports/insurance-types` | GET | — | List all insurance types |

---

### 2. **Prescription Endpoints**
| Name | Endpoint | Params | Description |
|------|-----------|---------|-------------|
| `get_contact_prescriptions` | `/patients/{patient_id}/prescriptions/contacts` | `patient_id` | Contact lens prescriptions for a patient |
| `get_frame_prescriptions` | `/patients/{patient_id}/prescriptions/frames` | `patient_id` | Frame prescriptions for a patient |

---

### 3. **Inventory Endpoints**
| Name | Endpoint | Params | Description |
|------|-----------|---------|-------------|
| `get_inventory` | `/inventory` | — | Retrieve entire frame/contact inventory |
| `get_frame_by_id` | `/inventory/frame/{frame_id}` | `frame_id` | Retrieve frame item details |
| `get_contact_by_id` | `/inventory/contact/{contact_id}` | `contact_id` | Retrieve contact lens item details |

---

### 4. **Retinal & Imaging**
| Name | Endpoint | Params | Description |
|------|-----------|---------|-------------|
| `get_retinal_scans` | `/patient/retinal_scans/{customer_id}` | `customer_id` | Retrieve all retinal scan metadata |
| `get_retinal_scan_image` | `/patient/retinal/scan/{filename}` | `filename` | Retrieve a single retinal scan image |
| `get_patient_image` | `/patients/image/{filename}` | `filename` | Retrieve a patient’s photo |
| `get_frame_image` | `/inventory/frame/image/{filename}` | `filename` | Retrieve a frame image |

---

### 5. **Appointments**
| Name | Endpoint | Params | Description |
|------|-----------|---------|-------------|
| `get_appointments` | `/appointments?start_date&end_date` | ISO 8601 date range | Retrieve appointments within range |
| `get_appointment_by_id` | `/appointments/{appointment_id}` | `appointment_id` | Retrieve single appointment |

---

### 6. **System and Diagnostics**
| Name | Endpoint | Params | Description |
|------|-----------|---------|-------------|
| `get_system_health` | `/api/health` | — | Backend + DB health check |
| `get_version` | `/api/version` | — | Get current system version |
| `get_connection_config` | `/admin/connections` | — | DB connection retry settings |
| `get_activity_summary` | `/activities/today-count` | — | Activity metrics |

---

## Authentication
- **JWT Bearer Token** required in headers.  
  Example:
