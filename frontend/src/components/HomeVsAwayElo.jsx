import React, {useState, useEffect} from "react"
import './../main.css'
import Select from 'react-select';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

export default function HomeVsAway () {


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
   
        fetch('http://localhost:8000/elo-home-vs-away/' + team.value)
        .then((res) => {
            return res.json();
        })
        .then((jsonData) => {
            var home = [];
            var away = [];
            jsonData.forEach((e) => {
                if (e.home_curr_elo) {
                    home.push(e.home_curr_elo); 
                }
                else {
                    away.push(e.away_curr_elo);
                }
            })

            var labels = [];
            for (var i = 0; i < Math.max(home.length, away.length); i++) {
                labels.push(i)
            }

            setData({
                labels: labels,
                datasets: [{
                    label: "Home ELO",
                    data: home
                },
                {
                    label: "Away ELO",
                    data: away
                }
                ]
            })
        })
    }


    return (
        <div className="chart-container">
            <h3>NBA 2022-23 Home vs Away ELO</h3>
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