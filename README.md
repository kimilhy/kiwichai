u need telegram api id and hash, character ai token and character id. 
how get character ai token: 

                                                                                                                                                                                    from characterai import aiocai, sendCode, authUser
    import asyncio

    async def main():
    email = input('YOUR EMAIL: ')

    code = sendCode(email)

    link = input('CODE IN MAIL: ')

    token = authUser(link, email)

    print(f'YOUR TOKEN: {token}')
    asyncio.run(main())

