import React from 'react';
import {withRouter} from 'react-router-dom'

const MessageContainer = ({ messages, loading, usersStack }) => {
  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
      <div>
        {messages.map(message => {
            return (
                <div className="container" key={message.id}>
                <table className="table table-hover">
                    <tbody>
                    <tr>
                        <td width="145px" height="145px">
                            <a href="" >
                                {/* <img src="#"/> */}
                                {usersStack.map((user, index) => {
                                    if (user.id === message.sender_id){
                                        return (
                                            <div key={user.id}>
                                            <img src={`${process.env.PUBLIC_URL}/assets/images/${user.image_file}`} width="90px" height="91px"/>
                                            <h6>{user.username}</h6>
                                            </div>
                                        )
                                    }

                                })}

                                    
                            </a>
                            
                        </td>
                        <td>
                            <span id="post{{ post.id }}">{message.body}</span>
                            <br></br>

                            <form action="/send_message/{{post.sender.username}}" method="POST">
                                <button className="btn btn-default match-button" name="match_profile" type="submit" value="{{post.sender.username}}">
                                Reply
                                </button>
                            </form>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            )
        })}
    </div>
  );
};

export default withRouter(MessageContainer);