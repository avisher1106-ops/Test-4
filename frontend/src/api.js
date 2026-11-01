export const API_BASE = "http://localhost:4000";

export async function fetchFruits(path) {
    const response = await fetch(`${API_BASE}${path}`, {
        headers: { Accept: "application/json" },
    });

    if (!response.ok) {
        throw new Error(`שגיאת שרת (${response.status})`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
        throw new Error("התקבלה תגובה לא תקינה מהשרת");
    }

    return data;
}
