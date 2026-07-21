import axios from "axios";
import { httpClient } from "./httpClient";
import type { PatientRequest, PopulationHealthResponse } from "../types/populationHealth";

const STRATIFY_ENDPOINT = "/population-health/stratify";

export async function stratifyPatient(
  request: PatientRequest,
): Promise<PopulationHealthResponse> {
  try {
    const { data } = await httpClient.post<PopulationHealthResponse>(
      STRATIFY_ENDPOINT,
      request,
    );
    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (!error.response) {
        throw new Error(
          "Unable to connect to http://127.0.0.1:8000/population-health/stratify. Verify the FastAPI service and CORS configuration.",
        );
      }
      const detail = error.response.data?.detail;
      throw new Error(
        typeof detail === "string"
          ? detail
          : `Population Health API request failed with status ${error.response.status}.`,
      );
    }
    throw error;
  }
}