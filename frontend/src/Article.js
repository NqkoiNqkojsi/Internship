import logo from './logo.svg';
import './Article.css';
import './App.css';
import React, { Component } from "react";
import { Link, Outlet, useParams } from "react-router-dom";
import axios from "axios";

function withParams(Component) {
	return props => <Component {...props} params={useParams()} />;
}


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
		this.state.entList.sort((a, b) => {
			if (a.entity_name.length === b.entity_name.length) {
				// Price is only important when cities are the same
				return b.occurences - a.occurences;
			 }
			return b.entity_name.length - a.entity_name.length;
		});
		this.state.entList.map((item) => {
			let lastOcc=0;
			for(let i=0;i<item.occurences;i++){
				let index = bodyEdit.indexOf(item.entity_name, lastOcc);
                if (index >= 0) { 
                    bodyEdit = bodyEdit.substring(0,index) + "<span class='highlight'>" + bodyEdit.substring(index,index+item.entity_name.length) + "</span>" + bodyEdit.substring(index + item.entity_name.length);
                }else{
                    break;
                }
                lastOcc=index +item.entity_name.length+30;
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
			<p className="artBody" id="artBody" dangerouslySetInnerHTML={{ __html:  bodyEdit}}>
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
			<tr className="rowNew" key={item.id}>      
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