import React, { Component } from 'react'
import axios from 'axios'
import {check} from './util/login'
import Alert from './Alert'
import {withRouter} from 'react-router-dom'

const btnreg = {
    fontSize: '12px',
    color: '#FFF',
    padding: '12px 18px',
    background: '#7f6681'
}
export class InterestForm extends Component {
    constructor(props){
        super(props)
        this.state = {
            err: '',
            allInterests: []
        }
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit = (event) => {
        event.preventDefault()
        const YourFavoriteProgrammingLanguage = event.target.elements.YourFavoriteProgrammingLanguage.value
        const SecondFavouriteProgrammingLanguage = event.target.elements.SecondFavouriteProgrammingLanguage.value
        const ChooseYourSpecialityDatabaseKnowledge = event.target.elements.ChooseYourSpecialityDatabaseKnowledge.value
        const FavoriteDatabaseManagementSystem = event.target.elements.FavoriteDatabaseManagementSystem.value
        const YourFieldOfInterest = event.target.elements.YourFieldOfInterest.value
        const WhichStatementBelowDescribesYouMostAccurately = event.target.elements.WhichStatementBelowDescribesYouMostAccurately.value
        const WhatisYourExperienceLevel = event.target.elements.WhatisYourExperienceLevel.value

        console.log(YourFavoriteProgrammingLanguage, SecondFavouriteProgrammingLanguage, ChooseYourSpecialityDatabaseKnowledge, FavoriteDatabaseManagementSystem, YourFieldOfInterest, WhichStatementBelowDescribesYouMostAccurately, WhatisYourExperienceLevel)

        const token = localStorage.getItem("token")
        
        console.log(token)
        axios.post('http://127.0.0.1:5000/api/add_interests', { 
            YourFavoriteProgrammingLanguage : YourFavoriteProgrammingLanguage,
            SecondFavouriteProgrammingLanguage : SecondFavouriteProgrammingLanguage,
            ChooseYourSpecialityDatabaseKnowledge : ChooseYourSpecialityDatabaseKnowledge,
            FavoriteDatabaseManagementSystem : FavoriteDatabaseManagementSystem,
            YourFieldOfInterest : YourFieldOfInterest,
            WhichStatementBelowDescribesYouMostAccurately: WhichStatementBelowDescribesYouMostAccurately,
            WhatisYourExperienceLevel: WhatisYourExperienceLevel,
        },
        {
            headers: {
                'Authorization': token
            }

        }).then((res) => {
            if (res.data.error) {
                this.setState({ err: res.data.error })
                console.log(res.data.error)
            }
            else {
                console.log(res.data)
                this.props.history.push('/')
            }
        })
    }

    

    componentDidMount() {
        const token = localStorage.getItem("token")
            axios.get('http://localhost:5000/api/get_interests', {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                }
            }).then(res => {
                if (res.data.error){
                    console.log(res.data.error)
                }
                else{
                this.setState({
                    allInterests: res.data.all_interests
                })
                console.log(res.data.users_stack)
                console.log(res.data.all_interests[3][1][0])
                
                 }
            });
        }
            
    

    render() {
        return (
            <div className="container">
                    <form 
                    onSubmitCapture={(event) => this.handleSubmit(
                        event
                    )} 
                    >
                    <fieldset className="form-group" style={{marginBottom: '-2px'}}>
                    {this.state.err.length > 0 && (
                        <Alert
                            message={`Check your form and try again! (${this.state.err})`}
                        />
                    )}
                    <div className="row">
                        <div className="col-xs-10 col-xs-offset-1">
                            <div className="panel panel-default" style={{padding: '20px'}}>
                            <div><h2>Add Interests</h2></div>
                            {this.state.allInterests.map((sub_interest, index) => {
                                return (
                                    <div key={index}>
                                    <h4>{sub_interest[0]}</h4>
                                    <div className="btn-group" data-toggle="buttons" style={{display: '-webkit-inline-box'}} key={index} >
                                        {sub_interest[1].map((interest, index) => {
                                            return (
                                                <label className="btn btn-sm" style={btnreg} key={index}>
                                                    <input
                                                    type="radio"
                                                    name={sub_interest[0].replace(/\s/g, "")}
                                                    value={interest[`${sub_interest[2]}id`]}
                                                    required
                                                    />
                                                    <label>{interest[`${sub_interest[2]}name`]}</label>
                                                </label>
                                            )
                                        })}
                                    </div>
                                    </div>
                                )
                            })}




                            {/* <h4>Your Favorite Programming Language</h4>
                            <div className="btn-group" style={{display: '-webkit-inline-box'}}>
                                <label className="btn btn-sm" style={btnreg}>
                                    <input
                                    type="radio"
                                    name="YourFavoriteProgrammingLanguage"
                                    value={this.state.YourFavouriteProgrammingLanguage}
                                    required
                                    />
                                    <label>Java</label>
                                

                                </label>
                            </div> */}
                            <p></p>
                            <input type="submit" value="submit" className="btn btn-success btn-lg btn-block" />

                        </div>
                        </div>
                    </div>
                    </fieldset>    

                </form>
                
            </div>
        )
    }
}

export default withRouter(InterestForm)
