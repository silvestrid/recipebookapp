import { useState, useEffect } from 'react';
import useSWR from 'swr'

import Header from './components/Header'
import RecipeList from './components/RecipeList';

import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const fetcher = (url, ...args) => fetch(`${BACKEND_URL}${url}`, ...args).then(res => res.json());

function App() {
  const [difficulty, setDifficulty] = useState('');
  const [filteredRecipes, setFilteredRecipes] = useState([]);
  const { data, error } = useSWR('/api/recipes', fetcher);

  const navigation = [
    { name: 'All Dishes', href: '#', current: true, onClick: () => { filterRecipes('') } },
    { name: 'Easy', href: '#', current: false, onClick: () => { filterRecipes('Easy') } },
    { name: 'Medium', href: '#', current: false, onClick: () => { filterRecipes('Medium') } },
    { name: 'Hard', href: '#', current: false, onClick: () => { filterRecipes('Hard') } },
  ]

  const filterRecipes = (level = undefined) => {
    if (!data) return;
    setDifficulty(level);
    setFilteredRecipes(
      data.recipes.filter(recipe => !level || recipe.difficulty.value === level)
    );
  }

  useEffect(() => {
    filterRecipes(difficulty);
  }, data);

  if (!error && !data)
    return <div>Loading...</div>;

  if (error)
    return <div>Failed to load recipes!</div>;

  return (
    <>
      <Header navigation={navigation} difficulty={difficulty || navigation[0].name} />
      <div className="bg-gray-100 max-w-7xl mx-auto sm:px-6 lg:px-8">
        <RecipeList recipes={filteredRecipes} />
      </div>
    </>
  );
}

export default App;
