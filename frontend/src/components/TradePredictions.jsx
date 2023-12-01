import React, {useState, useEffect} from "react"
import ReactTable from "react-table-6";
import "react-table-6/react-table.css";
import './../main.css'

export default function TradePredictions() {

    const [data, setData] = useState(null)
    const columns = [{
        Header: "Player Name",
        accessor: "player"
    },
    {
        Header: "Position",
        accessor: "position"
    },
    {
        Header: "New Team ELO Forecast",
        accessor: "prediction"
    }]

    useEffect(() => {
        let isUnmount = false;

        fetch('http://localhost:8000/predict')
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
            <h3>Player Trade Forecast</h3>
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