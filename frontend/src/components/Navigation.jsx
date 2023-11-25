import {Navbar, Nav, Container} from 'react-bootstrap';
import './../main.css';

export default function Navigation () {
    
    let textStyle = {
        color: "#fff",
        marginRight: 25
    }


    return (
        <Navbar className="navbar" expand="lg">
            <Container>
                <Navbar.Brand style={textStyle}>NBA ELO</Navbar.Brand>
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="ml-auto">
                        <Nav.Link className="navLink" href="/" style={textStyle}>Game Results</Nav.Link>
                    </Nav>

                    <Nav className="ml-auto">
                        <Nav.Link className="navLink" href="/team-elo-progression" style={textStyle}>ELO Progression</Nav.Link>
                    </Nav>

                    <Nav className="ml-auto">
                        <Nav.Link className="navLink" href="/team-elo-difference" style={textStyle}>ELO Difference</Nav.Link>
                    </Nav>

                    <Nav className="ml-auto">
                        <Nav.Link className="navLink" href="/best-matchups" style={textStyle}>Best Matchups</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}