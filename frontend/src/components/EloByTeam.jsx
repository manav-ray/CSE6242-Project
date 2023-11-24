import React, {useState, useEffect} from "react"
import './../main.css'
import Select from 'react-select';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

export default function EloByTeam () {

    const [selectedTeam, setSelectedTeam] = useState("-");
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
        setSelectedTeam(team.value)

        fetch('http://localhost:8000/elo/' + team.value)
        .then((res) => {
            return res.json();
        })
        .then((jsonData) => {
            var dates = [];
            var elos = [];
            jsonData.forEach((e) => {dates.push(e.date); elos.push(e.curr_elo)})


            setData({
                labels: dates,
                datasets: [{
                    label: "ELO Progression",
                    data: elos
                }]
            })
        })
    }


    return (
        <div className="lineCharts">
            <h3>NBA 2022-23 ELO Progression for {selectedTeam}</h3>
            <Select 
                onChange={selectHandler}
                options={teamOptions}
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