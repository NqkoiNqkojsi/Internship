import logo from './logo.svg';
import './Article.css';
import React, { Component } from "react";
import { Link, Outlet, useParams } from "react-router-dom";
import axios from "axios";


const article = {
        "id": 1,
        "date": null,
        "url": "https://gov.bg/bg/prestsentar/novini/%C2%A0borisov-temata-za-zapadnite-balkani-ne-tryabva-da-sliza-ot-evropeyskiya-dneven-red-ako-iskame-mir-i-stabilnost",
        "images": "/images/upload/13/768/2605-borissov-plenkovich-7.jpg",
        "videos": "",
        "title": "Борисов: Темата за Западните Балкани не трябва да слиза от европейския дневен ред, ако искаме мир и стабилност",
        "body": "Ако не гарантираме, че темата за Западните Балкани ще остане в дневния ред на Европейския съюз, тогава Срещата на върха в София е била просто една добра среща. Трябва да направим всичко възможно да не допуснем отново конфликт като този в бивша Югославия. Това са нашите Балкани, нашата Европа и затова трябва да положим огромни усилия. Така министър-председателят Бойко Борисов коментира постоянството, с което Българското председателство и лично той се ангажират с процеса на приобщаване на държавите от региона към Европа чрез постигане на свързаност, икономически растеж и разрешаване на двустранните конфликти. Той посочи, че е обсъдил темата и с папа Франциск при аудиенцията си вчера и е получил съгласието му да посети България, Румъния и при възможност и друга държава от региона с основната цел да изпрати послание за мир и разбирателство. Започнахме да решаваме проблемите в София и разчитаме на Хърватия да продължи процеса, каза Борисов. „Обединени можем да свършим много работа“, посочи той, като подчерта, че заедно с колегата си Пленкович се подкрепят при дискусиите в Европейския съвет, както и по темите, които се отнасят до общи проблеми в региона. На пресконференция след срещата си с хърватския премиер, по чиято покана е в Загреб, министър-председателят Бойко Борисов подчерта, че диалогът може да доведе до разбирателство, дори между държави с многогодишни проблеми помежду им. Той даде пример в новия етап в отношенията между България и Република Македония и разказа за поредното съвместно честване, обединило двете страни – отдаването на почит в Рим на делото на светите братя Кирил и Методий. Борисов благодари и за възможността броени дни след отбелязване на Празника на българската просвета и култура и на славянската писменост в хърватската столица да бъде открит паметник на патриарха на българската литература Иван Вазов, което е още един символ на близостта между страните и народите ни. Премиерът Пленкович поздрави министър-председателя Борисов за организираната Среща на върха в София, която постави темите за Западните Балкани след 15-годишна пауза. „Това беше послание към всички наши съседни държави да продължат с реформите, а съвместно с тях и да изграждаме свързаност - транспортна, дигитална инфраструктура“, коментира хърватският премиер. Той отбеляза чудесните политически и икономически отношения между Хърватия и България и подчерта, че ще продължи съвместното сътрудничество за влизане на страните в Шенгенското пространство и в еврозоната."
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
		this.generateArticle();
		this.generateList();
	}

	generateList = () => {
		let params = useParams();
		axios
		.get("http://localhost:8000/api/entArt?id_article="+params.artID)
		.then((res) => this.setState({ entList: res.data }))
		.catch((err) => console.log(err));
	};

	generateArticle = () => {
		let params = useParams();
		axios
		.get("http://localhost:8000/api/art/"+params.artID)
		.then((res) => this.setState({ article: res.data[0] }))
		.catch((err) => console.log(err));
	};

	displayCompleted = (status) => {
		if (status) {
		return this.setState({ viewCompleted: true });
		}

		return this.setState({ viewCompleted: false });
	};

	generateLinksEntities = (idEnt) => {
		console.log(idEnt);
	}

	renderArticle = () => {
		return (
		<div className="nav nav-tabs">
			<h1 class="ArtTitle">
				{ this.state.article.title }
			</h1>
			<a target="_blank" href={"https://gov.bg"+this.state.article["images"]}>
				<img class="img-thumbnail" src={"https://gov.bg"+this.state.article["images"]} alt="Thumbnail"></img>
			</a>
			<p class="artBody" id="artBody">
				{this.state.article.body}
			</p>
		</div>
		);
	};

	renderItems = () => {
		const { viewCompleted } = this.state;
		const newItems = this.state.todoList.filter(
		(item) => item.completed == viewCompleted
		);

		return newItems.map((item) => (
		<tr class="{% cycle 'row1' 'row2' %}" onclick="" id ="tableRows">      
			<td>{this.item.id_entity}</td>
			<td>{this.item.entity_name}</td>
			<td>{this.item.occurances}</td>
		</tr>
		));
	};

	render() {
		return (
		<main className="container">
			<div class="content-container">
			<div class="column" style="border-right:2px solid black; width:60%;">
				{this.renderArticle()}
			</div>
			<div class="column" style="width:32%;">
			<table>
				<tr>
					<td>ID</td>
				<td>Word</td>
				<td>Mentions</td>
				</tr> 
				{this.renderItems()}
			</table>              
			</div>
			</div>
		</main>
		);
	}
}



  
export default Article;