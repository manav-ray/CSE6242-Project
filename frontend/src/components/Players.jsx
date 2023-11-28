import React, {useState, useEffect} from "react"
import ReactTable from "react-table-6";
import "react-table-6/react-table.css";
import './../main.css'

export default function Players() {

    const [data, setData] = useState(null)
    const columns = [{
        Header: "Player Name",
        accessor: "name"
    },
    {
        Header: "Position",
        accessor: "position"
    },
    {
        Header: "Raptor WAR",
        accessor: "raptor_war"
    }]

    useEffect(() => {
        let isUnmount = false;

        fetch('http://localhost:8000/all-players')
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
            <h3>NBA 2022-23 Players</h3>
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