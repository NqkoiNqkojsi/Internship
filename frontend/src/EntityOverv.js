import logo from './logo.svg';
import './EntityOverv.css';
import './App.css';
import React, { Component } from "react";
import { Link, Outlet, useParams } from "react-router-dom";
import axios from "axios";

function withParams(Component) {
	return props => <Component {...props} params={useParams()} />;
}

function getArticleTitle(id){
    axios
    .get("../api/art/"+id)
    .then((result) => {return result.data.title;})
    .catch((err) => console.log(err));
}

class EntityOverv extends Component {
	constructor(props) {
		super(props);
		this.state = {
			viewCompleted: false,
			entArtList:[],
			entity :{"id": 1,
            "entity_name": "Борисов",
            "TotalOccurs": 2936,
            "MaxOccursinDoc": 11}
		};
	}

	componentDidMount() {
		this.generateEntity(this.props.params);
		this.generateList(this.props.params);
	}


	generateList = (params) => {
		axios
		.get("../api/entArt?id_entity="+params.entID)
		.then((res) => this.setState({ entArtList: res.data }))
		.catch((err) => console.log(err));
	};

	generateEntity = (params) => {
		axios
		.get("../api/ent/"+params.entID)
		.then((res) => this.setState({ entity: res.data}))
		.catch((err) => console.log(err));
	};

    generateArt = (id) => {
		axios
        .get("../api/art/"+id)
        .then((result) => {return result.data.title;})
        .catch((err) => console.log(err));
	};


	displayCompleted = (status) => {
		if (status) {
		return this.setState({ viewCompleted: true });
		}

		return this.setState({ viewCompleted: false });
	};

	renderEntity = () => {
		return (
            <div className="table-e-overv-container">
                <div className="table-legend label-table-name">Name:</div>
                <div className="table-legend label-table-total">Number of articles it appears in:</div>
                <div className="table-legend label-table-max-ment">Maximum number of mentions in an article:</div>
                <div className="table-legend label-table-doc-ment">Number of total occurences:</div>
                
                <div className="table-data">{this.state.entity.entity_name}</div>
                <div className="table-data">{this.state.entArtList.length}</div>
                <div className="table-data">{this.state.entity.MaxOccursinDoc}</div>
                <div className="table-data">{this.state.entity.TotalOccurs}</div>
            </div>
		);
	};

	renderItems = () => {
		this.state.entArtList.sort((a, b) => {
			if (a.occurences === b.occurences) {
				// Price is only important when cities are the same
				return a.id_article - b.id_article;
			 }
			return b.occurences - a.occurences;
		});
		return this.state.entArtList.map((item) => (
			<tr className="rowNew" key={item.id}>      
				<td>{item.id_article}</td>
				<td>{this.generateArt(item.id_article)}</td>
				<td>{item.occurences}</td>
			</tr>
		));
	};

	render() {
		return (
			<div className="content-container">
				<div className="heading-e-overv-container">
                    <h1 className="heading-e-overv">Entity Overview</h1>
                    <p className="par-e-overv">On this page you can find useful data about all entities, found throughout all the articles.</p>
                    <div className="heading-div"></div>
                </div>
                {this.renderEntity()}
                <h1>It appears in</h1>
				<div className="column2">
					<table>
						<tbody>
                            <tr>
                                <td>ID</td>
                                <td>Title</td>
                                <td>Occurences</td>
                            </tr>
							{this.renderItems()}
						</tbody>
					</table>              
				</div>
			</div>
		);
	}
}



  
export default withParams(EntityOverv);