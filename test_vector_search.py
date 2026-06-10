#!/usr/bin/env python3
"""
Comprehensive test suite for VectorSearchService.
"""

import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

from app.services.vector_search_service import VectorSearchService, TextEmbeddingProvider

print("\n" + "="*80)
print("VECTOR SEARCH SERVICE - COMPREHENSIVE TEST")
print("="*80)

# Test 1: Embedding Provider
print("\n[TEST 1] TextEmbeddingProvider Initialization")
try:
    provider = TextEmbeddingProvider()
    print(f"✓ Provider initialized")
    print(f"  - Backend: {provider.get_backend()}")
    print(f"  - Embedding Dimension: {provider.embedding_dim}")
    print(f"  - Model Name: {provider.model_name}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 2: Single text embedding
print("\n[TEST 2] Single Text Embedding")
try:
    test_text = "The quantum computing breakthrough revolutionizes cryptography research."
    embedding = provider.embed_single(test_text)
    print(f"✓ Text embedded successfully")
    print(f"  - Text: {test_text[:50]}...")
    print(f"  - Embedding shape: {embedding.shape}")
    print(f"  - Embedding dtype: {embedding.dtype}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 3: Batch text embedding
print("\n[TEST 3] Batch Text Embedding")
try:
    test_texts = [
        "AI chip startup raises $500M in funding.",
        "Tech giant announces major restructuring.",
        "Open-source framework gains significant traction."
    ]
    embeddings = provider.embed_texts(test_texts)
    print(f"✓ Batch embedding successful")
    print(f"  - Input texts: {len(test_texts)}")
    print(f"  - Output shape: {embeddings.shape}")
    print(f"  - Output dtype: {embeddings.dtype}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 4: VectorSearchService Initialization
print("\n[TEST 4] VectorSearchService Initialization")
try:
    vs = VectorSearchService()
    print(f"✓ Service initialized")
    print(f"  - Initialized: {vs.is_initialized()}")
    print(f"  - Index size: {vs.get_index_size()}")
    print(f"  - Stats: {vs.get_stats()}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 5: Single record indexing
print("\n[TEST 5] Single Stream Record Indexing")
try:
    success = vs.index_stream_record(db_id=1, text="Quantum computing breakthrough achieves 1000-qubit milestone.")
    print(f"✓ Record indexed: {success}")
    print(f"  - Index size after: {vs.get_index_size()}")
    print(f"  - DB ID mapping: {vs.vector_to_db_id}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 6: Batch record indexing
print("\n[TEST 6] Batch Record Indexing")
try:
    batch_records = [
        {"db_id": 2, "text": "AI startup raises $500 million in Series D funding round."},
        {"db_id": 3, "text": "Federal Reserve holds interest rates steady amid inflation concerns."},
        {"db_id": 4, "text": "Stock market rebounds sharply after disappointing earnings reports."},
        {"db_id": 5, "text": "Fortune 500 company commits to net-zero emissions by 2030."},
    ]
    count = vs.index_batch_records(batch_records)
    print(f"✓ Batch indexed successfully")
    print(f"  - Records indexed: {count}")
    print(f"  - Total index size: {vs.get_index_size()}")
    print(f"  - DB ID mapping length: {len(vs.vector_to_db_id)}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 7: Semantic search
print("\n[TEST 7] Semantic Search")
try:
    query = "quantum computing and cryptography"
    results = vs.semantic_search(query, top_k=3)
    print(f"✓ Semantic search complete")
    print(f"  - Query: {query}")
    print(f"  - Results returned: {len(results)}")
    for result in results:
        print(f"    - Rank {result['rank']}: db_id={result['db_id']}, "
              f"distance={result['distance']:.4f}, similarity={result['similarity']:.4f}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 8: Another semantic search
print("\n[TEST 8] Another Semantic Search Query")
try:
    query2 = "interest rates and economic policy"
    results2 = vs.semantic_search(query2, top_k=2)
    print(f"✓ Second search complete")
    print(f"  - Query: {query2}")
    print(f"  - Results returned: {len(results2)}")
    for result in results2:
        print(f"    - Rank {result['rank']}: db_id={result['db_id']}, similarity={result['similarity']:.4f}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 9: Error handling - invalid inputs
print("\n[TEST 9] Error Handling & Edge Cases")
try:
    # Empty text
    result = vs.index_stream_record(1, "")
    print(f"  ✓ Empty text handled: {result}")
    
    # Negative db_id
    result = vs.index_stream_record(-1, "test")
    print(f"  ✓ Negative db_id handled: {result}")
    
    # Empty batch
    count = vs.index_batch_records([])
    print(f"  ✓ Empty batch handled: {count} records")
    
    # Invalid batch record
    count = vs.index_batch_records([{"db_id": "invalid"}])
    print(f"  ✓ Invalid batch record handled: {count} records")
    
    # Empty query search
    results = vs.semantic_search("", top_k=5)
    print(f"  ✓ Empty query handled: {len(results)} results")
    
    print("✓ All error cases handled gracefully")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 10: Final statistics
print("\n[TEST 10] Final Service Statistics")
try:
    stats = vs.get_stats()
    print(f"✓ Statistics retrieved:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("ALL TESTS PASSED ✓")
print("="*80 + "\n")
