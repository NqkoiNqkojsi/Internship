import logo from './logo.svg';
import './Article.css';
import './App.css';
import React, { Component } from "react";
import { Link, Outlet, useParams } from "react-router-dom";
import axios from "axios";

function withParams(Component) {
	return props => <Component {...props} params={useParams()} />;
}


const entList=[{"id":1,"id_article":1,"id_entity":1,"entity_name":"Борисов","occurences":3},{"id":2,"id_article":1,"id_entity":2,"entity_name":"Европа","occurences":2},{"id":3,"id_article":1,"id_entity":3,"entity_name":"Франциск","occurences":1},{"id":4,"id_article":1,"id_entity":4,"entity_name":"Румъния","occurences":1},{"id":5,"id_article":1,"id_entity":5,"entity_name":"Методий","occurences":1},{"id":6,"id_article":1,"id_entity":6,"entity_name":"Бойко Борисов","occurences":2},{"id":7,"id_article":1,"id_entity":7,"entity_name":"Иван Вазов","occurences":1},{"id":8,"id_article":1,"id_entity":8,"entity_name":"София","occurences":3},{"id":9,"id_article":1,"id_entity":9,"entity_name":"България","occurences":3},{"id":10,"id_article":1,"id_entity":10,"entity_name":"Шенгенското","occurences":1},{"id":11,"id_article":1,"id_entity":11,"entity_name":"Югославия","occurences":1},{"id":12,"id_article":1,"id_entity":12,"entity_name":"Пленкович","occurences":2},{"id":13,"id_article":1,"id_entity":13,"entity_name":"Балкани","occurences":1},{"id":14,"id_article":1,"id_entity":14,"entity_name":"Кирил","occurences":1},{"id":15,"id_article":1,"id_entity":15,"entity_name":"Загреб","occurences":1},{"id":16,"id_article":1,"id_entity":16,"entity_name":"Хърватия","occurences":2},{"id":17,"id_article":1,"id_entity":17,"entity_name":"Европейския съвет","occurences":1},{"id":18,"id_article":1,"id_entity":18,"entity_name":"Европейския съюз","occurences":1},{"id":19,"id_article":1,"id_entity":19,"entity_name":"Рим","occurences":1},{"id":20,"id_article":1,"id_entity":20,"entity_name":"Българското председателство","occurences":1},{"id":21,"id_article":1,"id_entity":21,"entity_name":"Република Македония","occurences":1},{"id":22,"id_article":1,"id_entity":22,"entity_name":"Западните Балкани","occurences":2}];
class Article extends Component {
	constructor(props) {
		super(props);
		this.state = {
			viewCompleted: false,
			entList:[],
			article :{
				"id": null,
				"date": null,
				"url": "",
				"images": "",
				"videos": "",
				"title": "",
				"body": ""
			},
			id:0
		};
	}

	componentDidMount() {
		let { id } = this.props.params;
		console.log(id);
		this.generateArticle(this.props.params);
		this.generateList(this.props.params);
	}


	generateList = (params) => {
		console.log("params:");
		console.log(params);
		axios
		.get("../api/entArt?id_article="+params.artID)
		.then((res) => this.setState({ entList: res.data }))
		.catch((err) => console.log(err));
	};

	generateArticle = (params) => {
		axios
		.get("../api/art/"+params.artID)
		.then((res) => this.setState({ article: res.data}))
		.catch((err) => console.log(err));
	};

	sortList = (list) => {
		
	};

	displayCompleted = (status) => {
		if (status) {
		return this.setState({ viewCompleted: true });
		}

		return this.setState({ viewCompleted: false });
	};

	renderArticle = () => {
		let bodyEdit=this.state.article.body;
		this.state.entList.map((item) => {
			let lastOcc=0;
			for(let i=0;i<item.occurences;i++){
				let index = bodyEdit.indexOf(item.entity_name, lastOcc+30);
                if (index >= 0) { 
                    bodyEdit = bodyEdit.substring(0,index) + "<span class='highlight'>" + bodyEdit.substring(index,index+item.entity_name.length) + "</span>" + bodyEdit.substring(index + item.entity_name.length);
                }else{
                    break;
                }
                lastOcc=index +item.entity_name.length;
			}
		});
		return (
		<div className="nav nav-tabs">
			<h1 className="ArtTitle">
				{ this.state.article.title }
			</h1>
			<a target="_blank" href={"https://gov.bg"+this.state.article["images"]}>
				<img className="img-thumbnail" src={"https://gov.bg"+this.state.article["images"]} alt="Thumbnail"></img>
			</a>
			<p className="artBody" id="artBody">
				{bodyEdit}
			</p>
		</div>
		);
	};

	renderItems = () => {
		this.state.entList.sort((a, b) => {
			if (a.occurences === b.occurences) {
				// Price is only important when cities are the same
				return a.id_entity - b.id_entity;
			 }
			return b.occurences - a.occurences;
		});
		return this.state.entList.map((item) => (
			<tr className="{% cycle 'row1' 'row2' %}" key={item.id}>      
				<td>{item.id_entity}</td>
				<td>{item.entity_name}</td>
				<td>{item.occurences}</td>
			</tr>
		));
	};

	render() {
		return (
			<div className="content-container">
				<div className="column1">
					{this.renderArticle()}
				</div>
				<div className="column2">
					<table>
						<tbody>
							<tr>
								<td>ID</td>
								<td>Word</td>
								<td>Mentions</td>
							</tr> 
							{this.renderItems()}
						</tbody>
					</table>              
				</div>
			</div>
		);
	}
}



  
export default withParams(Article);