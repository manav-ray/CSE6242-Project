import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import EloByTeam from './components/EloByTeam';
import AllGames from './components/AllGames';
import Navigation from './components/Navigation';
import EloDifference from './components/EloDifference';
import BestMatchups from './components/BestMatchups';
import Players from './components/Players';

function App() {
  return (
    <Router>
      <Navigation />
      <Switch>
        <Route path="/" exact component={() => <AllGames />} />
        <Route path="/team-elo-progression" exact component={() => <EloByTeam />} />
        <Route path="/team-elo-difference" exact component={() => <EloDifference />} />
        <Route path="/best-matchups" exact component={() => <BestMatchups />} />
        <Route path="/players" exact component={() => <Players />} />
      </Switch>
    </Router>
  );
}

export default App;
