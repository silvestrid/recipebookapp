
import RecipeCard from './RecipeCard';

export default function RecipeList(props) {
    return (
        <main>
            <div className="px-4 py-8 md-px-16 grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3">
                {props.recipes.map((recipe) => {
                    return (
                        <RecipeCard key={recipe.id} recipe={recipe} />
                    );
                })}
            </div>
        </main>
    );
}