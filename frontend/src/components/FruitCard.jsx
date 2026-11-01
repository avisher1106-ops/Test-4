function formatNumber(value, unit) {
    return typeof value === "number" ? `${value} ${unit}` : "—";
}

export default function FruitCard({ fruit }) {
    const nutrition = fruit.nutritions || {};

    return (
        <article className="card">
            <div className="card-head">
                <h2>{fruit.name}</h2>
                <span className="badge">{nutrition.calories ?? "—"} קל׳</span>
            </div>

            <dl className="meta">
                <div>
                    <dt>משפחה</dt>
                    <dd>{fruit.family || "—"}</dd>
                </div>
                <div>
                    <dt>סוג</dt>
                    <dd>{fruit.genus || "—"}</dd>
                </div>
                <div>
                    <dt>סדרה</dt>
                    <dd>{fruit.order || "—"}</dd>
                </div>
                <div>
                    <dt>מזהה</dt>
                    <dd>{fruit.id ?? "—"}</dd>
                </div>
            </dl>

            <div className="nutrition">
                <div className="fat">
                    <span>שומן</span>
                    <strong>{formatNumber(nutrition.fat, "ג׳")}</strong>
                </div>
                <div className="sugar">
                    <span>סוכר</span>
                    <strong>{formatNumber(nutrition.sugar, "ג׳")}</strong>
                </div>
                <div className="carbs">
                    <span>פחמימות</span>
                    <strong>{formatNumber(nutrition.carbohydrates, "ג׳")}</strong>
                </div>
                <div className="protein">
                    <span>חלבון</span>
                    <strong>{formatNumber(nutrition.protein, "ג׳")}</strong>
                </div>
            </div>
        </article>
    );
}
