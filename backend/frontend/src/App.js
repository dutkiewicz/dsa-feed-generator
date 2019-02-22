import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid'
import Paper from '@material-ui/core/Paper'
import TextField from '@material-ui/core/TextField'
import InputLabel from '@material-ui/core/InputLabel'
import Button from '@material-ui/core/Button'
import LinearProgress from '@material-ui/core/LinearProgress'

import axios from 'axios'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const styles = {
  mainBox: {
    marginTop: '8em'
  },
  mainContent: {
    padding: '2em'
  },
  button: {
    marginTop: '1em',
    marginRight: '1em'
  }
}

class App extends Component {
  state = {
    url: null,
    id: null,
    file: null,
    processing: false
  }
  renderProcessing() {
    return this.state.processing ? <LinearProgress /> : null
  }

  renderButton() {
    let filepath = "/files/" + this.state.id

    if (this.state.file) {
      return (<Button 
                href={filepath}
                target="_blank"
                variant="contained"
                color="primary" 
                style={styles.button}>Download</Button>
              )
    } else {
      return (<Button 
                type="submit" 
                variant="contained" 
                color="default"
                disabled={this.state.processing}
                style={styles.button}>Generate feed</Button>)
    }
  }

  handleChangeUrl = e => {
    this.setState({url: e.target.value})
  }

  handleSubmit = e => {
    e.preventDefault();

    (async () => {
      const response = await axios.post("/api/v1/dsa/", {url: this.state.url});
      if (response.data.status === 'ok') {
        this.setState({id: response.data.id, processing: true})

        const getFile = setInterval(async () => {
          const res_file = await axios.get('/api/v1/dsa/' + this.state.id)
          if (res_file.data.status === 'done') {
            this.setState({file: res_file.data.feed.file, processing: false})
            clearInterval(getFile)
          }
        }, 1000)
      }
    })()
  }

  render() {
    return (
      <div className="App">
        <Grid container justify="center">
          <Grid item xs={12} lg={8} style={styles.mainBox}>
            <Paper style={styles.mainContent}>
              <form onSubmit={this.handleSubmit} method="POST">
                <InputLabel>Paste Google Shopping feed URL:</InputLabel>
                <TextField 
                  fullWidth 
                  name="url" 
                  type="url"
                  placeholder="http://" 
                  onChange={this.handleChangeUrl}
                  required/>
                {this.renderButton()}
              </form>
            </Paper>
              {this.renderProcessing()}
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default App;
