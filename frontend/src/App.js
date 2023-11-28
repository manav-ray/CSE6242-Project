import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import EloByTeam from './components/EloByTeam';
import AllGames from './components/AllGames';
import Navigation from './components/Navigation';
import EloDifference from './components/EloDifference';
import BestMatchups from './components/BestMatchups';
import Players from './components/Players';
import TradeEffect from './components/TradeEffect';
import EloMargin from './components/EloMargin';
import HomeVsAway from './components/HomeVsAwayElo';

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
        <Route path="/trade-effect" exact component={() => <TradeEffect />} />
        <Route path="/elo-margin-of-victory" exact component={() => <EloMargin />} />
        <Route path="/elo-home-vs-away" exact component={() => <HomeVsAway />} />
      </Switch>
    </Router>
  );
}

export default App;
