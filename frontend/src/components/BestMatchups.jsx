import React, {useState, useEffect} from "react"
import ReactTable from "react-table-6";
import "react-table-6/react-table.css";
import './../main.css'

export default function BestMatchups() {

    const [data, setData] = useState(null)
    const columns = [{
        Header: "Team One",
        accessor: "team1"
    },
    {
        Header: "Team Two",
        accessor: "team2"
    },
    {
        Header: "ELO Difference",
        accessor: "elo_difference"
    }]

    useEffect(() => {
        let isUnmount = false;

        fetch('http://localhost:8000/best-matchups')
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
            <h3>NBA 2023-24 Best Matchups</h3>
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