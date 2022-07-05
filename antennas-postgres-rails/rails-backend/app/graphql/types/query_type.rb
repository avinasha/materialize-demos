module Types
  class QueryType < Types::BaseObject
    # Add `node(id: ID!) and `nodes(ids: [ID!]!)`
    include GraphQL::Types::Relay::HasNodeField
    include GraphQL::Types::Relay::HasNodesField

    field :getAntennas, [Types::AntennaType], null: false,
      description: "Gets all the antennas."
    def getAntennas
      mdb = {
	      :host=>"localhost",
	      :port=>6875,
	      :user=>"materialize",
	      :password=>"materialize",
	      :dbname=>"materialize"
      }

      conn = PG.connect(mdb)
      result = conn.exec("SELECT * FROM antennas;");
      result.to_a
    end
  end
end
