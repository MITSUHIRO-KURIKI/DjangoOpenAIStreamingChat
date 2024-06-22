# from django.conf import settings
# from typing import List, Union
# from google.cloud.aiplatform_v1 import MatchServiceClient, IndexDatapoint, FindNeighborsRequest, FindNeighborsResponse
# from google.oauth2 import service_account
# import vertexai
# from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
# import openai
# from ..settings import IS_USE_EmbeddingVertexAi

# class VertexAiMatcher:

#     def __init__(self,
#                  PROJECT_ID:str,
#                  REGION:str,
#                  CREDENTIALS:service_account.Credentials,
#                  API_ENDPOINT:str,
#                  INDEX_ENDPOINT:str,
#                  DEPLOYED_INDEX_ID:str,
#                  ) -> Union[List[str], FindNeighborsResponse]:
#         # Verify the input is valid.
#         if not PROJECT_ID:
#             raise ValueError('Please set PROJECT_ID.')
#         if not REGION:
#             raise ValueError('Please set REGION.')
#         if not CREDENTIALS:
#             raise ValueError('Please set CREDENTIALS.')
#         if not API_ENDPOINT:
#             raise ValueError('Please set API_ENDPOINT.')
#         if not INDEX_ENDPOINT:
#             raise ValueError('Please set INDEX_ENDPOINT.')
#         if not DEPLOYED_INDEX_ID:
#             raise ValueError('Please set DEPLOYED_INDEX_ID.')
#         # Service Account によるGCP認証
#         vertexai.init(project=PROJECT_ID, location=REGION, credentials=CREDENTIALS)

#         self._index_endpoint      = INDEX_ENDPOINT
#         self._deployed_index_id   = DEPLOYED_INDEX_ID
#         # Service Account によるMatchServiceClient認証
#         self.vector_search_client = MatchServiceClient(
#                                       credentials    = CREDENTIALS,
#                                       client_options = {'api_endpoint': API_ENDPOINT},)

#     def get_similar(self,
#                     text:str,
#                     neighbor_count:int = 5,
#                     *,
#                     vertexai_embedding_model_name:str   = 'textembedding-gecko-multilingual@001',
#                     openai_embedding_model_name:str     = 'text-embedding-ada-002',
#                     datapoint_id:str                    = 'dummy-id',
#                     distance_thred:float                = 0.6,
#                     timeout:int                         = 60,
#                     isOnlyReturn_neighbors_id_list:bool = True,):
        
#         if IS_USE_EmbeddingVertexAi:
#             embedding = self.get_embedding_vertexai(text       = text,
#                                                     model_name = vertexai_embedding_model_name,)
#         else:
#             embedding = self.get_embedding_openai(text       = text,
#                                                   model_name = openai_embedding_model_name,
#                                                   timeout    = timeout,)
        
#         res = self.find_neighbors(embedding, neighbor_count, datapoint_id, distance_thred, isOnlyReturn_neighbors_id_list,)

#         return res

#     def get_embedding_vertexai(self,
#                                text:str,
#                                model_name:str,
#                                *,
#                                task_type:str  = 'RETRIEVAL_QUERY',
#                                title: str     = None,
#                                ) -> List[float]:

#         # Verify the input is valid.
#         if not model_name:
#             raise ValueError('Please set model_name.')
#         if not task_type:
#             raise ValueError('Please set task_type.')
#         if not text:
#             raise ValueError('Please set text.')
#         if title and task_type != 'RETRIEVAL_DOCUMENT':
#             raise ValueError('Title can only be provided if the task_type is RETRIEVAL_DOCUMENT')

#         """Generate text embedding with a Large Language Model."""
#         model = TextEmbeddingModel.from_pretrained(model_name)

#         text_embedding_input = TextEmbeddingInput(
#                                     task_type = task_type,
#                                     title     = title,
#                                     text      = text)

#         embeddings = model.get_embeddings([text_embedding_input])
#         embedding  = embeddings[0].values
#         return embedding

#     def get_embedding_openai(self,
#                              text:str,
#                              model_name:str,
#                              *,
#                              timeout:int,
#                              ) -> List[float]:
#         if not model_name:
#             raise ValueError('Please set model_name.')
#         if not text:
#             raise ValueError('Please set text.')

#         if settings.IS_USE_AZURE_OPENAI:
#             client = openai.AzureOpenAI(
#                                     azure_endpoint = settings.AZURE_OPENAI_ENDPOINT,
#                                     api_key        = settings.OPENAI_API_KEY,
#                                     api_version    = settings.AZURE_OPENAI_API_VERSION,
#                                     http_client    = None,) # IF USE ProxyServer httpx.Client(proxies=settings.HTTP_PROXY)
#         else:
#             client = openai.OpenAI(api_key     = settings.OPENAI_API_KEY,
#                                    http_client = None,) # IF USE ProxyServer httpx.Client(proxies=settings.HTTP_PROXY)
        
#         """Generate text embedding with a Large Language Model."""
#         responce  = client.embeddings.create(input   = text,
#                                              model   = model_name,
#                                              timeout = timeout,)
#         embedding = responce.data[0].embedding
        
#         return embedding
            

#     # Matching Engine にリクエストして、与えられたエンベディングの近似最近傍探索を行う
#     def find_neighbors(self,
#                        embedding:List[float],
#                        neighbor_count:int,
#                        datapoint_id:str,
#                        distance_thred:float,
#                        isOnlyReturn_neighbors_id_list:bool,
#                        ) -> Union[List[str], FindNeighborsResponse]:
#         # Verify the input is valid.
#         if not embedding:
#             raise ValueError('Please set embedding.')

#         datapoint = IndexDatapoint(
#             datapoint_id   = datapoint_id,
#             feature_vector = embedding
#         )
#         query   = FindNeighborsRequest.Query(
#                     datapoint      = datapoint,
#                     neighbor_count = neighbor_count,)
#         request = FindNeighborsRequest(
#                     index_endpoint    = self._index_endpoint,
#                     deployed_index_id = self._deployed_index_id,
#                     queries           = [query],)
#         res = self.vector_search_client.find_neighbors(request)

#         # datapoint_id のリストのみを返す場合の処理
#         if isOnlyReturn_neighbors_id_list:
#             return_id_list = []
#             # distance が distance_thred 以上の文書のみを返す
#             for neighbor in res.nearest_neighbors[0].neighbors:
#                 if neighbor.distance > distance_thred:
#                     return_id_list.append(neighbor.datapoint.datapoint_id)
#             return return_id_list
        
#         """
#         ## IF USE PSA IndexEndpoint
#         from google.cloud.aiplatform.matching_engine import MatchingEngineIndexEndpoint

#         def __init__():
#             self.index_endpoint = MatchingEngineIndexEndpoint(index_endpoint_name=INDEX_ENDPOINT)

#         def find_neighbors():
#             response = self.index_endpoint.match(
#                 deployed_index_id = self._deployed_index_id,
#                 queries           = [embedding],
#                 num_neighbros     = neighbor_count,)
#             neighbors = response[0]
#             if isOnlyReturn_neighbors_id_list:
#                 return_id_list = []
#                 for neighbor in neighbors:
#                     if neighbor.distance > distance_thred:
#                         return_id_list.append(neighbor.id)
#                 return return_id_list
#         """

#         return res