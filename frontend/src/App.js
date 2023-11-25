import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import EloByTeam from './components/EloByTeam';
import AllGames from './components/AllGames';
import Navigation from './components/Navigation';
import EloDifference from './components/EloDifference';

function App() {
  return (
    <Router>
      <Navigation />
      <Switch>
        <Route path="/" exact component={() => <AllGames />} />
        <Route path="/team-elo-progression" exact component={() => <EloByTeam />} />
        <Route path="/team-elo-difference" exact component={() => <EloDifference />} />
      </Switch>
    </Router>
  );
}

export default App;
