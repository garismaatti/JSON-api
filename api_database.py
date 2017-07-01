#!/usr/bin/env python2
# -*- coding: utf8 -*-
#
#
# Database for API
#
# 2017-04-24 by Ari Salopää
#

import sqlite


class Database(object):
	#
	#
	# Init script
	def __init__(self, dbName='./apiDatabase'):
		self._db = sqlite.connect( dbName + '.sqlite' )
		self._cur = self._db.cursor()
		print '[DB] DatabaseInit'
	#
	#
	# Check if taple already exist
	def _checkIfTableExist(self, tableName):
		# Check that debug DataBase table exist
		self._cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=:name ;', {'name': tableName})
		tableExist = self._cur.fetchall()
		if (len(tableExist) > 0):
			return True
		else:
			return False
	#
	#
	# create database
	def createDatabase(self):
		if not ( self._checkIfTableExist('Catalog') ):
			#Create table if it doesn't exist
			self._cur.execute( 'CREATE  TABLE  IF NOT EXISTS "main"."Catalog" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "name" TEXT NOT NULL , "amount" INTEGER NOT NULL , "price" FLOAT NOT NULL , "unit" TEXT DEFAULT ("kpl") , "currency" TEXT DEFAULT ("kpl"), "add_time" DATETIME NOT NULL  DEFAULT (DATETIME()), "add_person" TEXT NOT NULL , "mod_time" DATETIME NOT NULL  DEFAULT (DATETIME()), "mod_person" TEXT NOT NULL , "extra" TEXT);' )
			self._db.commit()
			print( "[DB][warning] Table 'Catalog' created to DB!" )
		#
		if not ( self._checkIfTableExist('Basket') ):
			#Create table if it doesn't exist
			self._cur.execute( 'CREATE  TABLE  IF NOT EXISTS "main"."Basket" ("user_id" TEXT PRIMARY KEY NOT NULL  UNIQUE , "product_id" INTEGER NOT NULL , "amount" INTEGER NOT NULL , "add_time" DATETIME NOT NULL  DEFAULT (DATETIME()), "mod_time" DATETIME NOT NULL  DEFAULT (DATETIME()), "extra" TEXT);' )
			self._db.commit()
			print( "[DB][warning] Table 'Basket' created to DB!" )
		#
		if not ( self._checkIfTableExist('Version') ):
			#Create table if it doesn't exist
			self._cur.execute( 'CREATE  TABLE  IF NOT EXISTS "main"."Version" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "version_number" FLOAT NOT NULL , "changes" TEXT NOT NULL , "add_time" DATETIME NOT NULL  DEFAULT (DATETIME()), "add_person" TEXT NOT NULL , "mod_time" DATETIME NOT NULL  DEFAULT (DATETIME()), "mod_person" TEXT NOT NULL , "extra" TEXT);' )
			self._db.commit()
			#Add current DB version
			self._cur.execute('INSERT INTO Version (id, version_number, changes, add_time, add_person, mod_time, mod_person) VALUES(NULL, ?, ?, DATETIME(), "my-database-library", DATETIME(), "my-database-library" )', (1.0, 'Initial version') )
			self._db.commit()
			print( "[DB][warning] Table 'Version' created to DB!" )
	#
	#
	#
	#
	# ###### GET ######
	#
	# Get full Catalog
	def get_full_catalog(self, fields={'id, name, amount, unit, price, currency, add_time, add_person, mod_time, mod_person, extra'):
		self._cur.execute('SELECT ' +fields +' FROM Catalog')
		return self._cur.fetchall()
	#
	# Get normal Catalog
	def get_catalog(self, fields={'id, name, amount, unit, price, currency'):
		self._cur.execute('SELECT ' +fields +' FROM Catalog')
		return self._cur.fetchall()
	#
	# Get full Basket
	def get_full_basket(self, fields={'user_id, product_id, amount, add_time, mod_time, extra'):
		self._cur.execute('SELECT ' +fields +' FROM Basket')
		return self._cur.fetchall()
	#
	# Get normal Basket
	def get_basket(self, fields={'user_id, product_id, amount'):
		self._cur.execute('SELECT ' +fields +' FROM Basket')
		return self._cur.fetchall()
	#
	#
	# Get all mangaonsites
	def getAllMangaOnsite(self, fields='id, id_Manga, id_Site, idOnSite, language, picSize, lastChecked, addTime, addPerson, modTime, modPerson, extra'):
		self._cur.execute('SELECT ' +fields +' FROM MangaOnSite ORDER BY lastChecked ASC ')
		return self._cur.fetchall()
	#
	#
	# Get all Chapters
	def getAllChapter(self, fields='id, id_MangaOnSite, id_Manga, onSiteChapterId, chapterNumber, id_DownloadStateCodes, isRead, addTime, addPerson, modTime, modPerson, extra'):
		self._cur.execute('SELECT ' +fields +' FROM Chapter')
		return self._cur.fetchall()
	#
	#
	# Get site script name from site
	def getAllMangaOnsite(self, fields='id, id_Manga, id_Site, idOnSite, language, picSize, lastChecked, addTime, addPerson, modTime, modPerson, extra'):
		self._cur.execute('SELECT ' +fields +' FROM MangaOnSite ORDER BY lastChecked ASC ')
		return self._cur.fetchall()
	#
	#
	# Super selector (select anything*)
	def getAnything(self, fields='id, id_Manga, id_Site, idOnSite, language, picSize, lastChecked, addTime, addPerson, modTime, modPerson, extra, nextUpdate', selector={}, fromTable='MangaOnSite'):
		# Make req
		sql_req = 'SELECT '
		sql_req += fields
		sql_req += ' FROM '
		sql_req += fromTable
		sql_req += ' WHERE 1 '
		for flName in selector:
			if ( selector.get(flName) ):
				sql_req += ' AND '
				sql_req += flName
				sql_req += '=:'
				sql_req += flName
				sql_req += ' '
		sql_req += ' ORDER BY id DESC LIMIT 1000;'
		self._cur.execute( sql_req, selector )
		#print('[DB] making any req:', sql_req, selector)
		return self._cur.fetchall()
	#
	#
	# Get all from Chapter id
	def getDownloadDataFromChapterId(self, cpid=-1):
		self._cur.execute('SELECT C.id, \
			C.id_MangaOnSite, \
			C.onSiteChapterId, \
			C.chapterNumber, \
			C.id_DownloadStateCodes, \
			O.id, \
			O.id_Manga, \
			O.id_Site, \
			O.language, \
			O.picSize, \
			M.id, \
			M.folderName, \
			S.id, \
			S.name, \
			S.siteScriptName, \
			C.episode, \
			O.idOnSite \
			FROM Chapter AS C \
			JOIN MangaOnSite AS O \
			ON O.id = C.id_MangaOnSite \
			JOIN Manga AS M \
			ON M.id = O.id_Manga \
			JOIN Site AS S \
			ON S.id = O.id_Site \
			WHERE C.id = :id ', {'id': cpid})
		return self._cur.fetchall()
	#
	#
	# Get Chapters with id_DownloadStateCodes between x & y (x&y included)
	def getChaptersWithStateBetween(self, fields='id, id_MangaOnSite, id_Manga, onSiteChapterId, chapterNumber, id_DownloadStateCodes, isRead, addTime, addPerson, modTime, modPerson, extra', fromNum=0, toNum=0):
		self._cur.execute('SELECT ' +fields +' FROM Chapter WHERE id_DownloadStateCodes BETWEEN :fm AND :to', {'fm': fromNum,'to': toNum})
		return self._cur.fetchall()
	#
	#
	# Get mangaonsites where nextUpdate <= today +null
	def getUpdateNeededMOS(self, fields='id, id_Manga, id_Site, idOnSite, language, picSize, lastChecked, addTime, addPerson, modTime, modPerson, extra, nextUpdate'):
		self._cur.execute('SELECT ' +fields +' FROM MangaOnSite WHERE nextUpdate <= DATETIME() UNION SELECT ' +fields +' FROM MangaOnSite WHERE IFNULL(nextUpdate,"") = "" ORDER BY lastChecked ASC ')
		return self._cur.fetchall()
	#
	#
	# Get mangaonsites where nextUpdate <= today, without null
	def getJustUpdateNeededMOS(self, fields='id, id_Manga, id_Site, idOnSite, language, picSize, lastChecked, addTime, addPerson, modTime, modPerson, extra, nextUpdate'):
		self._cur.execute('SELECT ' +fields +' FROM MangaOnSite WHERE nextUpdate < DATETIME() ORDER BY lastChecked ASC ')
		return self._cur.fetchall()
	#
	#
	# ###### ADD ######
	#
	#
	# add new Chapter
	def addChapter(self, dataBlob={}):
		self._cur.execute('INSERT INTO Chapter (id, id_MangaOnSite, id_Manga, onSiteChapterId, chapterNumber, id_DownloadStateCodes, isRead, addTime, addPerson, modTime, modPerson, extra, episode) VALUES (NULL, :id_MangaOnSite, :id_Manga, :onSiteChapterId, :chapterNumber, :id_DownloadStateCodes, :isRead, DATETIME(), :addPerson, DATETIME(), :modPerson, :extra, :episode )', dataBlob )
		self._db.commit()
		return self._cur.lastrowid
	#
	#
	# add new Manga
	def addManga(self, dataBlob={}):
		self._cur.execute('INSERT INTO Manga (id, jpnName, engName, folderName, infoSiteUrl, addTime, addPerson, modTime, modPerson, extra) VALUES (NULL, :jpnName, :engName, :folderName, :infoSiteUrl, DATETIME(), :addPerson, DATETIME(), :modPerson, :extra )', dataBlob )
		self._db.commit()
		return self._cur.lastrowid
	#
	#
	# add new MangaOnSite
	def addMangaOnSite(self, dataBlob={}):
		self._cur.execute('INSERT INTO "MangaOnSite" (id, id_Manga, id_Site, idOnSite, language, picSize, lastChecked, addTime, addPerson, modTime, modPerson, extra) VALUES (NULL, :id_Manga, :id_Site, :idOnSite, :language, :picSize, NULL, DATETIME(), :addPerson, DATETIME(), :modPerson, :extra )', dataBlob )
		self._db.commit()
		return self._cur.lastrowid
	#
	#
	#
	# ###### UPDATE ######
	#
	#
	# Update checked date on MOS
	def updateLastCheckedMOS(self, osid='', person='my-database-library'):
		self._cur.execute('UPDATE "MangaOnSite" SET "lastChecked" = DATETIME(), "modTime" = DATETIME(), modPerson = :pr WHERE "id" = :id', {'id': osid, 'pr': person})
		self._db.commit()
		return self._cur.lastrowid
	#
	#
	# Update after successfull dl
	def updateDownloadSuccess(self, dataBlob=''):
		self._cur.execute('UPDATE "Chapter" SET "id_DownloadStateCodes" = :id_DownloadStateCodes, modTime = DATETIME(), modPerson = :modPerson, extra = :extra WHERE "id" = :id_Capter', dataBlob )
		self._db.commit()
		return self._cur.lastrowid
	#
	#
	# Update nextUpdate to MOS
	def updateNextUpdateMOS(self, osid='', nextUpdate='', person='my-database-library'):
		self._cur.execute('UPDATE "MangaOnSite" SET "nextUpdate" = :nextup, "modTime" = DATETIME(), modPerson = :pr WHERE "id" = :id', {'id': osid, 'pr': person, 'nextup': nextUpdate})
		self._db.commit()
		return self._cur.lastrowid
	#
	#
	# Update Chapter to better chapter number
	def updateChapterNumber(self, idChapter='', newChapterNum='', person='my-database-library'):
		self._cur.execute('UPDATE "Chapter" SET "chapterNumber" = :newnum, "modTime" = DATETIME(), "modPerson" = :pr WHERE "id" = :id', {'id': idChapter, 'pr': person, 'newnum': newChapterNum})
		self._db.commit()
		return self._cur.lastrowid
	#
	#
	#
