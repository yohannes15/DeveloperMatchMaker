import React, { Component } from 'react'
import Alert from './Alert'

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
            YourFavouriteProgrammingLanguage: 'Java',
        }
    }
    render() {
        return (
            <div className="container">
                    <form 
                    onSubmitCapture={(event) => this.handleSubmit(
                        event, this.props.requestType
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

                            <h4>Your Favorite Programming Language</h4>
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
                            </div>
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

export default InterestForm
