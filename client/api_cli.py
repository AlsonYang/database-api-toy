'''
use commandline to send post request to the api endpoints. Need to run `python app.py` to run the api server first
'''
import click
import requests


@click.group()
def cli():
    """click group"""


@cli.command("get_members")
@click.option(
    "--ascending",
    default='true',
    help="return result in ascending order, true or false",
)
def get_members(ascending):
    '''send GET request to get all members'''
    click.echo(click.style("Send GET request to get all members"))
    api_response = requests.get(url="http://localhost:8080/members", params={'ascending': ascending})
    click.echo(click.style(f"response: {api_response.text}"))

@cli.command("get_member")
@click.option(
    "--id",
    prompt="enter id of the member",
    help="enter id of the member"
)
def get_member(id):
    '''send GET request to get member for a given id'''
    click.echo(click.style(f"Send GET request to get member for id `{id}`"))
    api_response = requests.get(url=f"http://localhost:8080/members/{id}")
    click.echo(click.style(f"response: {api_response.text}"))

@cli.command("post_member")
@click.option(
    "--data",
    prompt="Enter member information as json",
    help="Enter member information as json"
)
@click.option(
    "--capitalize_name",
    default='true',
    help="perform name capitalization true or false"
)
def post_member(data, capitalize_name):
    '''send POST request to add member for given data'''
    click.echo(click.style(f"Send POST request to create member with data `{data}`"))
    api_response = requests.post(url="http://localhost:8080/members", json=data, params={'capitalize_name': capitalize_name})
    click.echo(click.style(f"response: {api_response.text}"))

@cli.command("put_member")
@click.option(
    "--id",
    prompt="enter id of the member",
    help="enter id of the member"
)
@click.option(
    "--data",
    prompt="Enter member information as json",
    help="Enter member information as json"
)
def put_member(id, data):
    '''send PUT request to edit member for given data'''
    click.echo(click.style(f"Send PUT request to update id `{id}` with data `{data}`"))
    api_response = requests.put(url=f"http://localhost:8080/members/{id}", json=data)
    click.echo(click.style(f"response: {api_response.text}"))

@cli.command("delete_member")
@click.option(
    "--id",
    prompt="enter id of the member",
    help="enter id of the member"
)
def delete_member(id):
    '''send PUT request to edit member for given data'''
    click.echo(click.style(f"Send DELETE request to update member with id `{id}`"))
    api_response = requests.delete(url=f"http://localhost:8080/members/{id}")
    click.echo(click.style(f"response: {api_response.text}"))


if __name__=='__main__':
    cli()