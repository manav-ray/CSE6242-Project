import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import EloByTeam from './components/EloByTeam';
import AllGames from './components/AllGames';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={() => <AllGames />} />
        <Route path="/team-elo-progression" exact component={() => <EloByTeam />} />
      </Switch>
    </Router>
  );
}

export default App;
