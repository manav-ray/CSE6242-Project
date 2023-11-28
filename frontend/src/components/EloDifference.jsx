import React, {useState, useEffect} from "react";
import './../main.css';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

export default function EloDifference () {
    const [data, setData] = useState(null);

    useEffect(() => {
        let isUnmount = false;
        
        fetch('http://localhost:8000/elo-progression')
        .then((res) => {
            return res.json();
        })
        .then((jsonData) => {
            if (!isUnmount) {
                var teams = [];
                var preElos = [];
                var postElos = [];
                jsonData.forEach((e) => {teams.push(e.team); preElos.push(e.preElo); postElos.push(e.postElo); });

                setData({
                    labels: teams,
                    datasets: [{
                        label: "Pre-Season ELO",
                        data: preElos
                    },
                    {
                        label: "Post-Season ELO",
                        data: postElos                        
                    }]
                })
            }
        })

        return () => {
            isUnmount = true;
        }
    }, [])


    return (
        <div className="chart-container">
            <h3>NBA 2022-23 Pre to Post Season ELO Difference</h3>
            { data !== null ?
                <Bar 
                    data={data}
                />
                :
                <></>
            }
        </div>
    )
}