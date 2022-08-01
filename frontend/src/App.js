import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div>
      <h1 className="top-header">Welcome to the <span className="snt-br">Team Strawberry Project</span></h1>
      <p className="firstP">Our project provides entity analysis on the news, posted in <a className="link-norm link-gov" href="https://gov.bg/" target="_blank">gov.bg</a>.</p>
      <p className="secondP">This includes:</p>
      <p className="thirdP"> - Article by article reviews, showing which entities have been mentioned and how many times in a given document.</p>
      <p className="fourthP"> - Full overview of the entities, that have been mentioned across all articles, coupled with additional data.</p>
      <a className="btn btn-outline-danger button-upper" href="#" role="button">Go to articles</a>
      <a className="btn btn-outline-danger button-lower" href="#" role="button">Go to overview</a>
    </div>
  );
}

export default App;
