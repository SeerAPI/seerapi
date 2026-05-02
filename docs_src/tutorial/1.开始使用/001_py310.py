from seerapi import SeerAPI


async def main():
    async with SeerAPI() as client:
        skill = await client.get('skill', 38088)
        print(skill)
        print('\n')
        print('技能效果:\n' + '\n'.join([effect.info for effect in skill.skill_effect]))


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())