require 'test_helper'

class WordnetDiscoSemsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @wordnet_disco_sem = wordnet_disco_sems(:one)
  end

  test "should get index" do
    get wordnet_disco_sems_url
    assert_response :success
  end

  test "should get new" do
    get new_wordnet_disco_sem_url
    assert_response :success
  end

  test "should create wordnet_disco_sem" do
    assert_difference('WordnetDiscoSem.count') do
      post wordnet_disco_sems_url, params: { wordnet_disco_sem: { disco_result: @wordnet_disco_sem.disco_result, textb1: @wordnet_disco_sem.textb1, textb2: @wordnet_disco_sem.textb2, tfidf: @wordnet_disco_sem.tfidf, wordnet_result: @wordnet_disco_sem.wordnet_result } }
    end

    assert_redirected_to wordnet_disco_sem_url(WordnetDiscoSem.last)
  end

  test "should show wordnet_disco_sem" do
    get wordnet_disco_sem_url(@wordnet_disco_sem)
    assert_response :success
  end

  test "should get edit" do
    get edit_wordnet_disco_sem_url(@wordnet_disco_sem)
    assert_response :success
  end

  test "should update wordnet_disco_sem" do
    patch wordnet_disco_sem_url(@wordnet_disco_sem), params: { wordnet_disco_sem: { disco_result: @wordnet_disco_sem.disco_result, textb1: @wordnet_disco_sem.textb1, textb2: @wordnet_disco_sem.textb2, tfidf: @wordnet_disco_sem.tfidf, wordnet_result: @wordnet_disco_sem.wordnet_result } }
    assert_redirected_to wordnet_disco_sem_url(@wordnet_disco_sem)
  end

  test "should destroy wordnet_disco_sem" do
    assert_difference('WordnetDiscoSem.count', -1) do
      delete wordnet_disco_sem_url(@wordnet_disco_sem)
    end

    assert_redirected_to wordnet_disco_sems_url
  end
end
