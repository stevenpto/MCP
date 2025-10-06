"""MCP Server for Eye2Eye Patient Data API"""

from mcp.server.fastmcp import FastMCP
from typing import Optional
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("patients-api")

# Configuration
MAIN_API_BASE_URL = os.getenv("EYE2EYE_API_BASE_URL", "http://localhost:5005")
APPOINTMENTS_API_BASE_URL = os.getenv("EYE2EYE_APPOINTMENTS_API_BASE_URL", "http://localhost:5006")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
EYE2EYE_API_KEY = os.getenv("EYE2EYE_API_KEY")


async def make_request(url: str, method: str = "GET", params: Optional[dict] = None) -> dict:
    """
    Make HTTP request to the API and return JSON response.

    Args:
        url: Full URL to request
        method: HTTP method (default: GET)
        params: Optional query parameters

    Returns:
        Dictionary containing the response data or error
    """
    try:
        # Prepare headers with bearer token if available
        headers = {}
        if EYE2EYE_API_KEY:
            headers["Authorization"] = f"Bearer {EYE2EYE_API_KEY}"

        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            response = await client.request(method, url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {
            "error": f"HTTP {e.response.status_code}: {e.response.text}",
            "status_code": e.response.status_code
        }
    except httpx.RequestError as e:
        return {
            "error": f"Request failed: {str(e)}",
            "type": "connection_error"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "type": "unknown_error"
        }


# ============================================================================
# PATIENT ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_all_patients() -> dict:
    """
    Retrieve all patient profiles from the Eye2Eye system.

    Returns:
        Dictionary containing list of all patients with their complete information
    """
    url = f"{MAIN_API_BASE_URL}/patients"
    return await make_request(url)


@mcp.tool()
async def get_patient_by_id(patient_id: int) -> dict:
    """
    Retrieve a specific patient record by their ID.

    Args:
        patient_id: The unique patient identifier

    Returns:
        Dictionary containing the patient's complete record
    """
    url = f"{MAIN_API_BASE_URL}/patients/{patient_id}"
    return await make_request(url)


@mcp.tool()
async def get_patient_by_name(first_name: str, last_name: str) -> dict:
    """
    Search for a patient by their first and last name.

    Args:
        first_name: Patient's first name
        last_name: Patient's last name

    Returns:
        Dictionary containing matching patient record(s)
    """
    url = f"{MAIN_API_BASE_URL}/patient"
    params = {"first_name": first_name, "last_name": last_name}
    return await make_request(url, params=params)


@mcp.tool()
async def get_patients_by_birthday_month(month: int) -> dict:
    """
    Retrieve all patients with birthdays in a specific month.

    Args:
        month: Month number (1-12, where 1=January, 12=December)

    Returns:
        Dictionary containing list of patients with birthdays in the specified month
    """
    if month < 1 or month > 12:
        return {"error": "Month must be between 1 and 12", "type": "validation_error"}

    url = f"{MAIN_API_BASE_URL}/reports/birthday/{month}"
    return await make_request(url)


@mcp.tool()
async def get_patients_by_insurance_type(insurance_type: str) -> dict:
    """
    Filter patients by their insurance provider type.

    Args:
        insurance_type: The insurance provider name (e.g., "Blue Cross", "Aetna", "Medicare")

    Returns:
        Dictionary containing list of patients with the specified insurance type
    """
    url = f"{MAIN_API_BASE_URL}/reports/insurance"
    params = {"insurance_type": insurance_type}
    return await make_request(url, params=params)


@mcp.tool()
async def get_insurance_types() -> dict:
    """
    Retrieve a list of all insurance types/providers in the system.

    Returns:
        Dictionary containing list of all insurance provider types
    """
    url = f"{MAIN_API_BASE_URL}/reports/insurance-types"
    return await make_request(url)


# ============================================================================
# PRESCRIPTION ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_contact_prescriptions(patient_id: int) -> dict:
    """
    Retrieve all contact lens prescriptions for a specific patient.

    Args:
        patient_id: The unique patient identifier

    Returns:
        Dictionary containing list of contact lens prescriptions for the patient
    """
    url = f"{MAIN_API_BASE_URL}/patients/{patient_id}/prescriptions/contacts"
    return await make_request(url)


@mcp.tool()
async def get_frame_prescriptions(patient_id: int) -> dict:
    """
    Retrieve all eyeglass frame prescriptions for a specific patient.

    Args:
        patient_id: The unique patient identifier

    Returns:
        Dictionary containing list of frame prescriptions for the patient
    """
    url = f"{MAIN_API_BASE_URL}/patients/{patient_id}/prescriptions/frames"
    return await make_request(url)


# ============================================================================
# INVENTORY ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_inventory() -> dict:
    """
    Retrieve the complete inventory of frames and contact lenses.

    Returns:
        Dictionary containing all inventory items (frames and contacts)
    """
    url = f"{MAIN_API_BASE_URL}/inventory"
    return await make_request(url)


@mcp.tool()
async def get_frame_by_id(frame_id: int) -> dict:
    """
    Retrieve details of a specific frame from inventory.

    Args:
        frame_id: The unique frame identifier

    Returns:
        Dictionary containing the frame's details (brand, model, price, etc.)
    """
    url = f"{MAIN_API_BASE_URL}/inventory/frame/{frame_id}"
    return await make_request(url)


@mcp.tool()
async def get_contact_by_id(contact_id: int) -> dict:
    """
    Retrieve details of a specific contact lens from inventory.

    Args:
        contact_id: The unique contact lens identifier

    Returns:
        Dictionary containing the contact lens details (brand, type, parameters, etc.)
    """
    url = f"{MAIN_API_BASE_URL}/inventory/contact/{contact_id}"
    return await make_request(url)


# ============================================================================
# IMAGING ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_retinal_scans(customer_id: int) -> dict:
    """
    Retrieve all retinal scan metadata for a specific patient.

    Args:
        customer_id: The unique customer/patient identifier

    Returns:
        Dictionary containing list of retinal scan records with metadata
    """
    url = f"{MAIN_API_BASE_URL}/patient/retinal_scans/{customer_id}"
    return await make_request(url)


@mcp.tool()
async def get_retinal_scan_image(filename: str) -> dict:
    """
    Retrieve a specific retinal scan image file.

    Args:
        filename: The retinal scan image filename

    Returns:
        Dictionary containing the image data or download information
    """
    url = f"{MAIN_API_BASE_URL}/patient/retinal/scan/{filename}"
    return await make_request(url)


@mcp.tool()
async def get_patient_image(filename: str) -> dict:
    """
    Retrieve a patient's photo/image file.

    Args:
        filename: The patient image filename

    Returns:
        Dictionary containing the image data or download information
    """
    url = f"{MAIN_API_BASE_URL}/patients/image/{filename}"
    return await make_request(url)


@mcp.tool()
async def get_frame_image(filename: str) -> dict:
    """
    Retrieve a frame product image file.

    Args:
        filename: The frame image filename

    Returns:
        Dictionary containing the image data or download information
    """
    url = f"{MAIN_API_BASE_URL}/inventory/frame/image/{filename}"
    return await make_request(url)


# ============================================================================
# APPOINTMENTS ENDPOINTS (Separate API)
# ============================================================================

@mcp.tool()
async def get_appointments(start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
    """
    Retrieve appointments within a specified date range.

    Args:
        start_date: Start date in ISO 8601 format (YYYY-MM-DD) - optional
        end_date: End date in ISO 8601 format (YYYY-MM-DD) - optional

    Returns:
        Dictionary containing list of appointments within the date range
    """
    url = f"{APPOINTMENTS_API_BASE_URL}/appointments"
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return await make_request(url, params=params)


@mcp.tool()
async def get_appointment_by_id(appointment_id: int) -> dict:
    """
    Retrieve a specific appointment by its ID.

    Args:
        appointment_id: The unique appointment identifier

    Returns:
        Dictionary containing the appointment details
    """
    url = f"{APPOINTMENTS_API_BASE_URL}/appointments/{appointment_id}"
    return await make_request(url)


# ============================================================================
# ACTIVITIES ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_recent_activities(limit: int = 4) -> dict:
    """
    Retrieve the most recent activities for dashboard display.

    Args:
        limit: Maximum number of recent activities to return (default: 4)

    Returns:
        Dictionary containing list of recent activities
    """
    url = f"{MAIN_API_BASE_URL}/activities/recent"
    params = {"limit": limit}
    return await make_request(url, params=params)


@mcp.tool()
async def get_all_activities(limit: int = 50, start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
    """
    Retrieve all activities with optional pagination and date filtering.

    Args:
        limit: Maximum number of activities to return (default: 50)
        start_date: Start date in ISO 8601 format (YYYY-MM-DD) - optional
        end_date: End date in ISO 8601 format (YYYY-MM-DD) - optional

    Returns:
        Dictionary containing list of activities
    """
    url = f"{MAIN_API_BASE_URL}/activities"
    params = {"limit": limit}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return await make_request(url, params=params)


@mcp.tool()
async def get_today_activities_count() -> dict:
    """
    Get the count of activities that occurred today.

    Returns:
        Dictionary containing the count of today's activities
    """
    url = f"{MAIN_API_BASE_URL}/activities/today-count"
    return await make_request(url)


# ============================================================================
# SYSTEM & DIAGNOSTICS ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_system_health() -> dict:
    """
    Check the health status of the backend system and database connectivity.

    Returns:
        Dictionary containing health status, database connection status, and timestamp
    """
    url = f"{MAIN_API_BASE_URL}/api/health"
    return await make_request(url)


@mcp.tool()
async def get_system_version() -> dict:
    """
    Get the current version of the Eye2Eye backend system.

    Returns:
        Dictionary containing version information
    """
    url = f"{MAIN_API_BASE_URL}/api/version"
    return await make_request(url)


@mcp.tool()
async def get_connection_config() -> dict:
    """
    Get database connection configuration and retry settings.

    Returns:
        Dictionary containing connection approach, retry settings, and configuration notes
    """
    url = f"{MAIN_API_BASE_URL}/admin/connections"
    return await make_request(url)


# Entry point for running the server
if __name__ == "__main__":
    mcp.run()
