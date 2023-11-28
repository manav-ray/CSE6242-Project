import React, {useState, useEffect} from "react"
import './../main.css'
import Select from 'react-select';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

export default function EloMargin () {


    const [teamOptions, setTeamOptions] = useState([]);
    const [data, setData] = useState(null);

    useEffect(() => {
        let isUnmount = false;

        fetch('http://localhost:8000/all-teams')
        .then((res) => {
            return res.json();
        })
        .then((jsonData) => {
            if (!isUnmount) {
                var tempArr = [];
                jsonData.teams.forEach((team) => {
                    tempArr.push({
                        value: team, label: team
                    })
                })
                setTeamOptions(tempArr)
            }
        })

        return () => {
            isUnmount = true;
        }
    }, [])


    const selectHandler = (team) => {
        if (team.length <= 0) {
            setData(null)
            return;
        } 
   
        fetch('http://localhost:8000/elo-margin-of-victory/' + team.value)
        .then((res) => {
            return res.json();
        })
        .then((jsonData) => {
            var dates = [];
            var elos = [];
            var scores = []
            jsonData.forEach((e) => {dates.push(e.date); elos.push(e.curr_elo); scores.push(e.score_diff)})


            setData({
                labels: dates,
                datasets: [{
                    label: "Normalized ELO",
                    data: elos
                },
                {
                    label: "Normalized Score",
                    data: scores
                }
                ]
            })
        })
    }


    return (
        <div className="chart-container">
            <h3>NBA 2022-23 ELO vs Score Difference</h3>
            <Select 
                onChange={selectHandler}
                options={teamOptions}
                isClearable={false}
                isSearchable={true}
            />
            { data !== null ?
                <Line 
                    data={data}
                />
                :
                <></>
            }
        </div>
    )
}