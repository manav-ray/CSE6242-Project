import React, {useState, useEffect} from "react"
import './../main.css'
import Select from 'react-select';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

export default function EloByTeam () {

    var colorArray = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];


    const [selectedTeams, setSelectedTeams] = useState([]);
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


    const selectHandler = (teams) => {
        if (teams.length <= 0) {
            setSelectedTeams([])
            setData(null)
            return;
        } else if (teams.length === 1) {
            fetch('http://localhost:8000/elo/' + teams[0].value)
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
                        label: teams[0].value + " Progression",
                        data: elos,
                        backgroundColor: colorArray[teams.length - 1],
                        borderColor: colorArray[teams.length - 1]
                    }]
                })
            })
            setSelectedTeams(teams)
        } else {
            if (teams.length > selectedTeams.length) {
                const diff = teams.filter(x => !selectedTeams.includes(x))
    
                fetch('http://localhost:8000/elo/' + diff[0].value)
                .then((res) => {
                    return res.json();
                })
                .then((jsonData) => {
                    var dates = [];
                    var elos = [];
                    jsonData.forEach((e) => {dates.push(e.date); elos.push(e.curr_elo)})
        
                    if (dates.length > data.labels.length) {
                        setData({
                            labels: dates,
                            datasets: [...data.datasets, {
                                label: diff[0].value + " Progression",
                                data: elos,
                                backgroundColor: colorArray[teams.length - 1],
                                borderColor: colorArray[teams.length - 1]
                            }]
                        })
                    } else {
                        setData({
                            labels: data.labels,
                            datasets: [...data.datasets, {
                                label: diff[0].value + " Progression",
                                data: elos,
                                backgroundColor: colorArray[teams.length - 1],
                                borderColor: colorArray[teams.length - 1]
                            }]
                        })  
                    }
    
                })
    
            } else {
                const diff = selectedTeams.filter(x => !teams.includes(x))
                const deleted = diff[0].value
                setData({
                    labels: data.labels,
                    datasets: data.datasets.filter(function(team) {
                        return !team.label.includes(deleted)
                    })
                })
            }
            setSelectedTeams(teams)
        }
    }


    return (
        <div className="chart-container">
            <h3>NBA 2022-23 ELO Progression</h3>
            <Select 
                value={selectedTeams}
                onChange={selectHandler}
                options={teamOptions}
                isMulti={true}
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