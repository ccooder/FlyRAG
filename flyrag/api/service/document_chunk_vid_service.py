#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/7 17:09
from typing import List

from langchain_weaviate import WeaviateVectorStore
from sqlalchemy import delete
from sqlmodel import Session, select

import common
from common.mysql_client import MysqlClient
from common.weaviate_client import WeaviateClient
from flyrag.api.entity import DocumentChunkVid, DocumentChunkVidQuery


class DocumentChunkVidService(object):
    @staticmethod
    def create_chunk_vid(chunk_vids: List[DocumentChunkVid], session: Session):
        session.add_all(chunk_vids)
        session.commit()

    @staticmethod
    def list_vids(vid_query: DocumentChunkVidQuery,  session: Session, offset: int=0, limit: int=1000):
        statement = MysqlClient.fill_statement(select(DocumentChunkVid).offset(offset).limit(limit), DocumentChunkVid, vid_query)
        # 如果有自定义查询字段，请在此自行添加
        if vid_query.doc_id:
            statement = statement.where(DocumentChunkVid.doc_id == vid_query.doc_id)
        if vid_query.chunk_id:
            statement = statement.where(DocumentChunkVid.chunk_id == vid_query.chunk_id)
        vids = session.exec(statement).all()
        return vids

    @staticmethod
    async def delete_vids(vid_query: DocumentChunkVidQuery, session: Session, autocommit: bool = True):

        doc_vids = DocumentChunkVidService.list_vids(vid_query, session)
        # 遍历删除向量数据库的关联向量
        with WeaviateClient().get_client() as weaviate_client:
            wvs = WeaviateVectorStore(client=weaviate_client, index_name=common.DEFAULT_WEAVIATE_COLLECTION,
                                      text_key='text')
            ids = []
            for doc_vid in doc_vids:
                ids.extend(doc_vid.vids.split(','))
            if len(ids) > 0:
                await wvs.adelete(ids)

        statement = MysqlClient.fill_statement(delete(DocumentChunkVid), DocumentChunkVid, vid_query)
        # 如果有自定义查询字段，请在此自行添加
        if vid_query.doc_id:
            statement = statement.where(DocumentChunkVid.doc_id == vid_query.doc_id)
        if vid_query.chunk_id:
            statement = statement.where(DocumentChunkVid.chunk_id == vid_query.chunk_id)
        result = session.exec(statement)

        if autocommit:
            session.commit()
        return result.rowcount

if __name__ == '__main__':
    DocumentChunkVidService.delete_vids(DocumentChunkVidQuery(chunk_id=564992074743681026), next(MysqlClient().get_session()))
