from database.models import Site, Setting, Site_Setting, session
from sqlalchemy import select
from middleware.config import log

class SettingService:

    def addSetting(name, base_value):
        setting = Setting(name=name, base_value=base_value)
        session.add(setting)
        session.commit()
        return setting.serialize()

    def getAll():
        setting = select(Setting)
        result = session.execute(setting).scalars().all()
        return [res.serialize() for res in result]

    def get_by_id(id):
        return Setting.get_by_id(id)

    def get_by_name(name):
        stmt = select(Setting).where(Setting.name == name)
        setting = session.execute(stmt).scalars().one_or_none()
        return setting.serialize()

    def add_value(value, site_id, setting_id):
        sett = session.execute(select(Site_Setting)
        .where(Site_Setting.setting_id == setting_id)
        .where(Site_Setting.site_id == site_id)).scalars().one_or_none()
        if sett:
            sett.value = value
            session.add(sett)
            session.commit()
            return sett.serialize()
        else:
            setting = Site_Setting(value=value, site_id=site_id, setting_id=setting_id)
            session.add(setting)
            session.commit()
            return setting.serialize()

    def update_setting(name, base_value):
        setting = session.execute(
            select(Setting)
            .where(Setting.name == name)
        ).scalars().one_or_none()
        setting.base_value = base_value
        session.add(setting)
        session.commit()
        return setting.serialize()


    
    def delete_setting(id):
        try:
            site = session.execute(select(Setting).where(Setting.id == id)).scalars().one_or_none()
            if site:
                session.delete(site)
                session.commit()
                return dict(error = "All Right")
            else:
                return dict(error = "Setting doesn't exist")
        except Exception as e:
            log.error(e)
            return dict(error = e)

    def get_value_settings(site_id=None, name=None, url=None):
        if site_id:
            site = select(Site).where(Site.id == site_id)
        if name:
            site = select(Site).where(Site.name == name)
        if url:
            site = select(Site).where(Site.url == url)
        site = session.execute(site).scalars().one_or_none()
        if site:
            stmt = select(Site_Setting).where(Site_Setting.site_id == site.id)
            setting = session.execute(stmt).scalars().all()
            return [sett.serialize() for sett in setting]
        else:
            return dict(error = "Site doesn't exist")