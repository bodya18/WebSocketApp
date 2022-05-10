from database.models import Site, session
from sqlalchemy import select, delete
from middleware.config import log

class SiteService:

    def addSite(name, url, status = None):
        site = Site(name=name, url=url, status=status)
        session.add(site)
        session.commit()
        return site.serialize()

    def getAll():
        site = select(Site)
        result = session.execute(site).scalars().all()
        return [res.serialize() for res in result]

    def get_by_id(id):
        return Site.get_by_id(id)

    def get_by_name(name):
        stmt = select(Site).where(Site.name == name)
        site = session.execute(stmt).scalars().one_or_none()
        return site.serialize() if site else site

    def get_by_url(url):
        stmt = select(Site).where(Site.url == url)
        site = session.execute(stmt).scalars().one_or_none()
        return site.serialize() if site else site

    def delete_site(id):
        try:
            site = session.execute(select(Site).where(Site.id == id)).scalars().one_or_none()
            if site:
                session.delete(site)
                session.commit()
                return "All Right"
            else:
                return dict(error = "Site doesn't exist")
        except Exception as e:
            log.error(e)
            return dict(error = e)
        