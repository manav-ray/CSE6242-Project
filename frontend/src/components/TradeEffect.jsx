import React, {useState, useEffect} from "react"
import ReactTable from "react-table-6";
import "react-table-6/react-table.css";
import './../main.css'

export default function TradeEffect() {

    const [data, setData] = useState(null)
    const columns = [{
        Header: "Player",
        accessor: "player"
    },
    {
        Header: "Old Team",
        accessor: "old_team"
    },
    {
        Header: "New Team",
        accessor: "new_team"
    },
    {
        Header: "Old Team Pre ELO",
        accessor: "old_team_pre"
    },
    {
        Header: "Old Team Post ELO",
        accessor: "old_team_post"
    },
    {
        Header: "Old Team Difference",
        accessor: "old_difference"
    },
    {
        Header: "New Team Pre ELO",
        accessor: "new_team_pre"
    },
    {
        Header: "New Team Post ELO",
        accessor: "new_team_post"
    },
    {
        Header: "New Team Difference",
        accessor: "new_difference"
    }]

    useEffect(() => {
        let isUnmount = false;

        fetch('http://localhost:8000/trade-effect')
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
            <h3>NBA 2022-23 Player Trade Effects</h3>
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