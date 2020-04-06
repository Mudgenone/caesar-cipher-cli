import click
import requests
import json
import hashlib

@click.group()
def main():
    """
    Solving the caesar cipher challenge of codenation
    """
    pass

@main.command()
@click.option('-t', '--token', required=True, type=str)
def challenge(token):
    click.echo('Get challenge json...')

    link_api = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data'
    ploads = {'token': token}

    answer = requests.get(url=link_api, params=ploads)

    click.echo('Challenge:')
    click.echo(answer.content)

    click.echo('Saving on file...')
    with open('answer.json', 'wb') as f:
        f.write(answer.content)
    click.echo('Done.')

@main.command()
@click.argument('filename', type=click.Path(exists=True))
def decrypt(filename):
    # Open file
    filename = click.format_filename(filename)
    with open(filename) as f:
        data = json.load(f)

    click.echo('Decrypt message...')
    message = getDecryptMessage(data['cifrado'], data['numero_casas'])
    hashSHA1 = getSHA1Hash(message)
    showMessage = 'Decryped: ' + message
    showSHA1 = 'SHA1: ' + hashSHA1
    click.echo('-' * len(showMessage))
    click.echo(showMessage)
    click.echo(showSHA1)
    click.echo('-' * len(showMessage))

    click.echo('Saving on JSON...')
    data['decifrado'] = message
    data['resumo_criptografico'] = hashSHA1
    saveJSON(filename, data)

    click.echo('Done.')

@main.command()
@click.option('-t', '--token', required=True, type=str)
@click.argument('filename', type=click.Path(exists=True))
def send(token, filename):
    # Open file
    filename = click.format_filename(filename)

    click.echo('Sending challenge json...')

    link_api = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution'
    ploads = {'token': token}
    files = {'answer': open(filename, 'rb')}

    score = requests.post(url=link_api, params=ploads, files=files)
    
    click.echo('Status:' + str(score.status_code))
    click.echo('Score:')
    click.echo(score.content)

    click.echo('Done.')


def getDecryptMessage(message, key):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # letters to ints and the inverse
    L2I = dict(zip(alphabet,range(26)))
    I2L = dict(zip(range(26), alphabet))

    decrypt = ''

    for symbol in message.lower():
        if symbol.isalpha():
            decrypt += I2L[(L2I[symbol] - key) % 26]
        else:
            decrypt += symbol

    return decrypt

def saveJSON(filename, newJSON):
    file = open(filename, 'w')
    json.dump(newJSON, file)
    file.close()

def getSHA1Hash(text):
    sha1 = hashlib.sha1()
    sha1.update(text.encode())
    return sha1.hexdigest()


if __name__ == '__main__':
    main()
