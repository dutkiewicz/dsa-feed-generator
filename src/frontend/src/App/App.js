import React, { Component } from 'react';
import { Grid, Paper, TextField, Button, LinearProgress, Typography } from '@material-ui/core'
import classes from './App.module.css'
import axios from '../axios/axios'


class App extends Component {
  state = {
    url: '',
    feed_id: null,
    location: '',
    processing: false,
    errorMsg: ''
  }
  renderProgress() {
    return this.state.processing ? <LinearProgress /> : null
  }

  renderError() {
    if (this.state.errorMsg) {
      return (
        <div className={classes.ErrorMessage}>
          <Typography variant="inherit">{this.state.errorMsg}</Typography>
        </div>
      )
    }
  }

  renderButton() {
    if (this.state.location && !this.state.processing) {
      return (
        <div className={classes.Btn}>
          <Button href={this.state.location} target="_blank" variant="contained" color="primary">Download</Button>
          <Button className={classes.Reset} variant="contained" color="default" onClick={this.handleReset}>Reset</Button>
        </div>
      )
    }

    if (!this.state.processing) {
      return (
        <div className={classes.Btn}>
          <Button type="submit" variant="contained" color="default">Generate DSA Page feed</Button>
        </div>
      )
    }

    if (this.state.processing) {
      return (
        <div className={classes.Btn}>
          <Button type="submit" variant="contained" color="default" disabled>Processing...</Button>
        </div>
      )
    }
  }

  handleReset = e => {
    this.setState({ url: '', errorMsg: '', location: '' })
  }

  handleChangeUrl = e => {
    this.setState({ url: e.target.value })
  }

  handleSubmit = e => {
    e.preventDefault();
    this.setState({ processing: true, errorMsg: '' })

    axios.post('api/v1/feeds/', { url: this.state.url })
      .then(response => {
        this.setState({ feed_id: response.data.id })
      })
      .then(() => {
        console.log('requesting operation')
        const getFeedStatus = setInterval(() => axios.get('api/v1/feeds/' + this.state.feed_id)
          .then(response => {
            if (response.data.status === 'finished') {
              this.setState({ location: response.data.location, processing: false })
              clearInterval(getFeedStatus)
            }
          })
          .catch(error => this.setState({ errorMsg: error.message, processing: false }))
          , 1000)

      })
      .catch(error => this.setState({ errorMsg: error.message, processing: false }))
  }

  render() {
    return (
      <Grid container justify="center" className={classes.MainBox}>
        <Grid item xs={12} lg={8}>
          <Paper className={classes.MainContent}>
            <form onSubmit={this.handleSubmit} method="POST">
              <TextField
                fullWidth
                label="Paste Google Merchant Center feed URL"
                name="url"
                type="url"
                placeholder="http://domain.com/merchant-center-feed.xml"
                onChange={this.handleChangeUrl}
                required />

              {this.renderButton()}
            </form>

            {this.renderError()}
          </Paper>
          {this.renderProgress()}
        </Grid>
      </Grid>
    );
  }
}

export default App;
