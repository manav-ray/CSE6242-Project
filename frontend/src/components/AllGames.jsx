import React, {useState, useEffect} from "react"
import ReactTable from "react-table-6";
import "react-table-6/react-table.css";
import './../main.css'

export default function AllGames() {

    const [data, setData] = useState(null)
    const columns = [{
        Header: "Home Team",
        accessor: "homeTeam"
    },
    {
        Header: "Away Team",
        accessor: "awayTeam"
    },
    {
        Header: "Playoff",
        accessor: "playoff"
    },
    {
        Header: "Home Score",
        accessor: "homeScore"
    },
    {
        Header: "Away Score",
        accessor: "awayScore"
    },
    {
        Header: "Date",
        accessor: "date"
    }]

    useEffect(() => {
        let isUnmount = false;

        fetch('http://localhost:8000/all-games')
        .then((res) => {
            return res.json();
        })
        .then((jsonData) => {
            if (!isUnmount) {
                setData(jsonData)
            }
        })

        return () => {
            isUnmount = true;
        }
    }, [])

    return (
        <div className="chart-container">
            <h3>NBA 2022-23 Season Game Results</h3>
            { data !== null ?
                <ReactTable 
                    data={data}
                    columns={columns}
                    defaultPageSize={100}
                    style={{
                      height: "800px" 
                    }}
                    className="-striped -highlight"
                />
                :
                <></>
            }
        </div>
    )
}