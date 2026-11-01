import { useEffect, useRef, useState } from "react";

import { API_BASE, fetchFruits } from "./api";
import FruitCard from "./components/FruitCard";

const TABS = [
    { id: "all", label: "כל הפירות", icon: "🧺" },
    { id: "search", label: "חיפוש", icon: "🔍" },
    { id: "calories", label: "לפי קלוריות", icon: "🔥" },
];

const INITIAL_STATUS = {
    message: "טוען את כל הפירות...",
    isError: false,
    count: null,
};

export default function App() {
    const [activeTab, setActiveTab] = useState("all");
    const [fruits, setFruits] = useState([]);
    const [status, setStatus] = useState(INITIAL_STATUS);
    const [loading, setLoading] = useState(false);
    const [emptyMessage, setEmptyMessage] = useState("");
    const [searchTerm, setSearchTerm] = useState("");
    const [calories, setCalories] = useState("");
    const searchInputRef = useRef(null);
    const caloriesInputRef = useRef(null);
    const requestIdRef = useRef(0);

    async function load(path, { emptyMessage: empty, successMessage }) {
        const currentRequest = ++requestIdRef.current;
        setLoading(true);
        setStatus({ message: "טוען נתונים...", isError: false, count: null });

        try {
            const data = await fetchFruits(path);
            if (currentRequest !== requestIdRef.current) {
                return;
            }

            setFruits(data);
            setEmptyMessage(empty);
            setStatus({
                message: successMessage,
                isError: false,
                count: data.length,
            });
        } catch (error) {
            if (currentRequest !== requestIdRef.current) {
                return;
            }

            setFruits([]);
            setEmptyMessage("");
            setStatus({
                message: `שגיאה: ${error.message}. ודאו ששרת ה-API פועל בכתובת ${API_BASE}`,
                isError: true,
                count: null,
            });
        } finally {
            if (currentRequest === requestIdRef.current) {
                setLoading(false);
            }
        }
    }

    function loadAllFruits() {
        load("/api/fruits", {
            emptyMessage: "לא התקבלו פירות מהשרת.",
            successMessage: "כל הפירות נטענו בהצלחה",
        });
    }

    useEffect(() => {
        loadAllFruits();
    }, []);

    function activateTab(tabId) {
        setActiveTab(tabId);

        if (tabId === "all") {
            loadAllFruits();
        } else if (tabId === "search") {
            searchInputRef.current?.focus();
        } else {
            caloriesInputRef.current?.focus();
        }
    }

    function handleSearch(event) {
        event.preventDefault();
        const query = searchTerm.trim();

        if (!query) {
            setStatus({ message: "יש להזין טקסט לחיפוש", isError: true, count: null });
            searchInputRef.current?.focus();
            return;
        }

        load(`/api/search/${encodeURIComponent(query)}`, {
            emptyMessage: `לא נמצא פרי בשם "${query}".`,
            successMessage: `תוצאות חיפוש עבור "${query}"`,
        });
    }

    function handleCalories(event) {
        event.preventDefault();
        const rawValue = calories.trim();

        if (rawValue === "" || Number(rawValue) < 0) {
            setStatus({
                message: "יש להזין מספר קלוריות תקין (0 ומעלה)",
                isError: true,
                count: null,
            });
            caloriesInputRef.current?.focus();
            return;
        }

        load(`/api/calories/${encodeURIComponent(rawValue)}`, {
            emptyMessage: `אין פירות עם עד ${rawValue} קלוריות.`,
            successMessage: `פירות עם עד ${rawValue} קלוריות`,
        });
    }

    return (
        <div className="page">
            <header className="hero">
                <div className="hero-icon">🍉</div>
                <h1>Fruity API</h1>
                <p>
                    מידע חי על פירות מתוך <span dir="ltr">Fruityvice</span> — חיפוש, קלוריות וערכים תזונתיים
                </p>
            </header>

            <main>
                <section className="controls" aria-label="בקרות">
                    <div className="tabs" role="tablist" aria-label="בחירת פעולה">
                        {TABS.map((tab) => (
                            <button
                                key={tab.id}
                                type="button"
                                className={`tab ${activeTab === tab.id ? "active" : ""}`}
                                role="tab"
                                aria-selected={activeTab === tab.id}
                                aria-controls={`panel-${tab.id}`}
                                onClick={() => activateTab(tab.id)}
                            >
                                <span aria-hidden="true">{tab.icon}</span> {tab.label}
                            </button>
                        ))}
                    </div>

                    <div
                        className={`panel ${activeTab === "all" ? "" : "hidden"}`}
                        id="panel-all"
                        role="tabpanel"
                    >
                        <p className="panel-hint">טוען את כל הפירות הזמינים ב-API.</p>
                        <button
                            type="button"
                            className="btn"
                            onClick={loadAllFruits}
                            disabled={loading}
                        >
                            טען את כל הפירות
                        </button>
                    </div>

                    <div
                        className={`panel ${activeTab === "search" ? "" : "hidden"}`}
                        id="panel-search"
                        role="tabpanel"
                    >
                        <form className="search-form" onSubmit={handleSearch}>
                            <label className="sr-only" htmlFor="search-input">
                                חיפוש פרי לפי שם
                            </label>
                            <input
                                type="text"
                                id="search-input"
                                ref={searchInputRef}
                                placeholder="חפש פרי, למשל: apple"
                                autoComplete="off"
                                value={searchTerm}
                                onChange={(event) => setSearchTerm(event.target.value)}
                            />
                            <button type="submit" className="btn" disabled={loading}>
                                חיפוש
                            </button>
                        </form>
                        <p className="panel-hint">
                            החיפוש מתבצע לפי שם הפרי ואינו תלוי באותיות גדולות או קטנות.
                        </p>
                    </div>

                    <div
                        className={`panel ${activeTab === "calories" ? "" : "hidden"}`}
                        id="panel-calories"
                        role="tabpanel"
                    >
                        <form className="search-form" onSubmit={handleCalories}>
                            <label className="sr-only" htmlFor="calories-input">
                                מקסימום קלוריות
                            </label>
                            <input
                                type="number"
                                id="calories-input"
                                ref={caloriesInputRef}
                                min="0"
                                step="1"
                                placeholder="מקסימום קלוריות, למשל: 50"
                                value={calories}
                                onChange={(event) => setCalories(event.target.value)}
                            />
                            <button type="submit" className="btn" disabled={loading}>
                                סינון
                            </button>
                        </form>
                        <p className="panel-hint">
                            יוצגו כל הפירות שערכם הקלורי קטן או שווה לערך שהוזן.
                        </p>
                    </div>
                </section>

                <div
                    className={`status ${status.isError ? "error" : ""}`}
                    role="status"
                    aria-live="polite"
                >
                    {status.message}
                    {status.count !== null && (
                        <span className="count">{status.count} תוצאות</span>
                    )}
                </div>

                <section className="results" aria-label="תוצאות">
                    {fruits.map((fruit) => (
                        <FruitCard key={`${fruit.id}-${fruit.name}`} fruit={fruit} />
                    ))}

                    {!loading && emptyMessage && fruits.length === 0 && (
                        <div className="empty">
                            <span className="emoji">🍽️</span>
                            <h3>לא נמצאו תוצאות</h3>
                            <p>{emptyMessage}</p>
                        </div>
                    )}
                </section>
            </main>

            <footer>
                <span>REST API מקומי:</span>
                <code dir="ltr">{API_BASE}</code>
                <span className="footer-sep">•</span>
                <a href={`${API_BASE}/docs`} target="_blank" rel="noopener">
                    תיעוד Swagger
                </a>
                <span className="footer-sep">•</span>
                <a href="http://localhost:8082" target="_blank" rel="noopener">
                    ניהול מסד נתונים
                </a>
            </footer>
        </div>
    );
}
